"""Evaluate the selected checkpoint once on the reserved test manifest."""
import argparse
import json
from pathlib import Path
import torch
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix
from torch.utils.data import Dataset, DataLoader
from torchvision.models import EfficientNet_B0_Weights
from app.ml.training.train_cnn import create_model, getDevice

ML_DIR = Path(__file__).resolve().parent
class HeldOutImages(Dataset):
    def __init__(self, names, labels):
        self.names, self.labels = names, labels
        self.transform = EfficientNet_B0_Weights.IMAGENET1K_V1.transforms()
    def __len__(self): return len(self.names)
    def __getitem__(self, index):
        path = ML_DIR / self.names[index]
        with Image.open(path) as image:
            tensor = self.transform(image.convert('RGB'))
        return tensor, self.labels.index(path.parent.name)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--checkpoint',type=Path,default=ML_DIR/'models/plant_model_v1.pt')
    parser.add_argument('--manifest',type=Path,default=ML_DIR/'reports/splits.json')
    args=parser.parse_args()
    checkpoint=torch.load(args.checkpoint,map_location='cpu',weights_only=True)
    labels=checkpoint['labels']; names=json.loads(args.manifest.read_text())['test']
    device=getDevice(); torch.set_num_threads(4)
    model=create_model(len(labels),pretrained=False).to(device)
    model.load_state_dict(checkpoint['model_state_dict']); model.eval()
    truth=[]; predictions=[]; confidence=[]
    with torch.inference_mode():
        for images, targets in DataLoader(HeldOutImages(names,labels),batch_size=64,num_workers=4):
            probability=model(images.to(device)).softmax(1).cpu()
            truth.extend(targets.tolist()); predictions.extend(probability.argmax(1).tolist()); confidence.extend(probability.max(1).values.tolist())
    report={'model_version':checkpoint['model_version'],'checkpoint_epoch':checkpoint['epoch'],'test_images':len(names),
            'classification_report':classification_report(truth,predictions,labels=list(range(len(labels))),target_names=labels,output_dict=True,zero_division=0),
            'confusion_matrix':confusion_matrix(truth,predictions,labels=list(range(len(labels)))).tolist(),'label_order':labels,
            'confidence_thresholds':{str(threshold):{'coverage':sum(c>=threshold for c in confidence)/len(confidence),'accuracy_when_accepted':sum(t==p for t,p,c in zip(truth,predictions,confidence) if c>=threshold)/max(1,sum(c>=threshold for c in confidence))} for threshold in (.5,.7,.9)},
            'limitations':'Held-out images from the same source dataset, not an independent real-world study. Confidence is not calibrated. Exact duplicates removed; near duplicates may remain.'}
    output=ML_DIR/'reports/test_evaluation.json'; output.write_text(json.dumps(report,indent=2)); print(json.dumps(report,indent=2))
if __name__ == '__main__': main()
