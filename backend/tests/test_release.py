"""API regression tests use an isolated database and upload directory."""
import io
from contextlib import closing
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

_temp = tempfile.TemporaryDirectory()
os.environ['STORAGE_DIR'] = _temp.name
os.environ['DATABASE_URL'] = f'sqlite:///{_temp.name}/test.db'
os.environ['ADMIN_TOKEN'] = 'test-admin-token'
from fastapi.testclient import TestClient
from PIL import Image
from app.main import app
from app.db.session import Base, engine
from app.core.security import _requests
from app.ml import inference

class ReleaseTests(unittest.TestCase):
    def setUp(self):
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        _requests.clear()
        self.client = TestClient(app)
        self.auth = {'Authorization': 'Bearer test-admin-token'}

    def image(self):
        output = io.BytesIO()
        Image.new('RGB', (64, 64), 'green').save(output, format='PNG')
        return output.getvalue()

    def predict(self):
        with patch('app.services.prediction_service.run_inference', return_value={'plant_state':'leaf_spots','confidence':.65,'model_version':'test-v1'}):
            return self.client.post('/api/v1/predict', files={'file':('leaf.png',self.image(),'image/png')})

    def test_upload_history_review_and_metrics(self):
        response = self.predict()
        self.assertEqual(response.status_code,200,response.text)
        prediction = response.json()
        self.assertTrue(prediction['needs_review'])
        self.assertEqual(self.client.get('/api/v1/predictions').status_code,401)
        history = self.client.get('/api/v1/predictions',headers=self.auth).json()
        self.assertEqual(len(history),1)
        self.assertNotIn('image_path',history[0])
        pid=prediction['prediction_id']
        self.assertEqual(self.client.get(f'/api/v1/reviews/{pid}/image').status_code,401)
        self.assertEqual(self.client.get(f'/api/v1/reviews/{pid}/image',headers=self.auth).status_code,200)
        self.assertEqual(self.client.post(f'/api/v1/reviews/{pid}',headers=self.auth,json={'correct_label':'invented'}).status_code,422)
        review=self.client.post(f'/api/v1/reviews/{pid}',headers=self.auth,json={'correct_label':'healthy'})
        self.assertEqual(review.status_code,200,review.text)
        self.assertEqual(self.client.get('/api/v1/reviews',headers=self.auth).json(),[])
        self.assertEqual(self.client.get('/api/v1/metrics/summary',headers=self.auth).json()['total_predictions'],1)
        self.assertEqual(self.client.get('/metrics/summary',headers=self.auth).status_code,200)

    def test_upload_rejection_and_failure_cleanup(self):
        self.assertEqual(self.client.post('/api/v1/predict',files={'file':('bad.png',b'broken','image/png')}).status_code,400)
        self.assertEqual(self.client.post('/api/v1/predict',files={'file':('big.png',b'x'*(5*1024*1024+1),'image/png')}).status_code,413)
        directory=Path(_temp.name)/'uploaded_images'
        before=set(directory.glob('*'))
        with patch('app.services.prediction_service.run_inference',side_effect=RuntimeError('no checkpoint')):
            self.assertEqual(self.client.post('/api/v1/predict',files={'file':('leaf.png',self.image(),'image/png')}).status_code,503)
        self.assertEqual(before,set(directory.glob('*')))

    def test_admin_unconfigured_fails_closed(self):
        with patch.dict(os.environ,{'ADMIN_TOKEN':''}):
            self.assertEqual(self.client.get('/api/v1/reviews',headers=self.auth).status_code,503)

    def test_rate_limit(self):
        for _ in range(10):
            self.assertEqual(self.client.post('/api/v1/predict',files={'file':('bad.txt',b'x')}).status_code,400)
        self.assertEqual(self.client.post('/api/v1/predict',files={'file':('bad.txt',b'x')}).status_code,429)

    def test_readiness_is_not_liveness(self):
        self.assertEqual(self.client.get('/health').status_code,200)
        with patch('app.api.v1.routes_health.load_model',side_effect=RuntimeError('missing')):
            self.assertEqual(self.client.get('/ready').status_code,503)

    def test_review_export_backup_and_retention(self):
        from app.maintenance import export_reviews, backup_database, purge
        from app.db.session import SessionLocal
        from app.db.models import PredictionLog
        from datetime import UTC, datetime, timedelta
        import json
        import sqlite3
        prediction = self.predict().json()
        pid = prediction['prediction_id']
        self.client.post(f'/api/v1/reviews/{pid}', headers=self.auth, json={'correct_label':'healthy'})
        with tempfile.TemporaryDirectory() as output:
            destination = Path(output)
            export_reviews(destination / 'export')
            manifest = json.loads((destination / 'export/manifest.json').read_text())
            self.assertEqual(manifest[0]['label'], 'healthy')
            self.assertTrue((destination / 'export' / manifest[0]['image']).is_file())
            backup_database(destination / 'backup.db')
            with closing(sqlite3.connect(destination / 'backup.db')) as saved:
                self.assertEqual(saved.execute('select count(*) from prediction_logs').fetchone()[0], 1)
            with SessionLocal() as db:
                row = db.get(PredictionLog, pid)
                row.created_at = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=60)
                image = Path(row.image_path)
                db.commit()
            purge(30, False, True)
            self.assertTrue(image.exists())
            purge(30, True, False)
            self.assertTrue(image.exists())
            purge(30, True, True)
            self.assertFalse(image.exists())

    def test_real_checkpoint_contract_and_inference(self):
        import torch
        from torchvision.models import efficientnet_b0
        torch.set_num_threads(2)
        model=efficientnet_b0(weights=None)
        model.classifier[1]=torch.nn.Linear(model.classifier[1].in_features,3)
        labels=['healthy','leaf_spots','severe_damage']
        checkpoint={'model_state_dict':model.state_dict(),'architecture':'efficientnet_b0','labels':labels,'class_to_idx':dict(zip(labels,range(3))), 'pretrained_weights':'IMAGENET1K_V1','image_size':224,'model_version':'test-model'}
        path=Path(_temp.name)/'model.pt'; torch.save(checkpoint,path)
        image=Path(_temp.name)/'image.png'; image.write_bytes(self.image())
        inference.load_model.cache_clear()
        try:
            with patch.object(inference,'MODEL_PATH',path):
                result=inference.run_inference(str(image))
                self.assertIn(result['plant_state'],labels)
                self.assertTrue(0 <= result['confidence'] <= 1)
                self.assertEqual(result['model_version'],'test-model')
                inference.load_model.cache_clear()
                checkpoint['labels']=list(reversed(labels)); torch.save(checkpoint,path)
                with self.assertRaises(RuntimeError): inference.load_model()
        finally:
            inference.load_model.cache_clear()

if __name__ == '__main__': unittest.main()
