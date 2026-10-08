import unittest
import tempfile
import json
from pathlib import Path
from unittest.mock import patch
import torch
from torch.utils.data import DataLoader, TensorDataset
from app.ml.training import train_cnn as training
from app.ml import audit_dataset

class TrainingTests(unittest.TestCase):
    def test_frozen_features_and_fine_tuning(self):
        torch.set_num_threads(2)
        model=training.create_model(3,pretrained=False)
        loader=DataLoader(TensorDataset(torch.rand(2,3,64,64),torch.tensor([0,2])),batch_size=2)
        optimizer=torch.optim.AdamW(model.parameters(),lr=.001)
        scaler=torch.amp.GradScaler('cuda',enabled=False)
        bn=next(m for m in model.features.modules() if isinstance(m,torch.nn.BatchNorm2d))
        before=bn.running_mean.clone(); head=model.classifier[1].weight.detach().clone()
        training.train_one_epoch(model,loader,torch.nn.CrossEntropyLoss(),optimizer,torch.device('cpu'),scaler)
        self.assertTrue(torch.equal(before,bn.running_mean))
        self.assertFalse(torch.equal(head,model.classifier[1].weight))
        self.assertTrue(all(p.grad is None for p in model.features.parameters()))
        training.set_fine_tuning(model,True)
        training.train_one_epoch(model,loader,torch.nn.CrossEntropyLoss(),optimizer,torch.device('cpu'),scaler)
        self.assertTrue(any(p.grad is not None for p in model.features.parameters()))

    def test_audit_removes_cross_split_duplicates_without_touching_sources(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name); (root/'labels.json').write_text('["healthy"]')
            for split in ('train','val'): (root/'data'/split/'healthy').mkdir(parents=True)
            (root/'data/train/healthy/a.png').write_bytes(b'a')
            (root/'data/val/healthy/duplicate.png').write_bytes(b'a')
            (root/'data/val/healthy/b.png').write_bytes(b'b')
            (root/'data/val/healthy/c.png').write_bytes(b'c')
            with patch.object(audit_dataset,'ML_DIR',root),patch.object(audit_dataset,'REPORTS',root/'reports'):
                audit_dataset.main()
                manifest=json.loads((root/'reports/splits.json').read_text())
                self.assertEqual({key:len(value) for key,value in manifest.items()},{'train':1,'val':1,'test':1})
                self.assertTrue((root/'data/val/healthy/duplicate.png').exists())

if __name__=='__main__': unittest.main()
