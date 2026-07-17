
from pathhlib import Path  #ease of use for files
import json # who is json?

import torch
from torch import nn # neural networks :D
from torch.utils.data import DataLoader # optimizing how data is loaded
from torchvision import datasets, transforms, models # ease of use for training
from sklearn.metrics import accuracy_score, f1_score # quantification of results
from tqdm import tqdm # for loading bars
# main ML folder
ML_DIR = Path(__file__).resolve().parent
# training image storage
TRAIN_DIR = ML_DIR / "data" / "train"
# validation image storage
VAL_DIR = ML_DIR / "data" / "val"

# where trained models are saved :D
MODELS_DIR = ML_DIR / "models"
MODELS_DIR.mkdir(exist_ok=True)
# model file name
MODEL_PATH = MODELS_DIR / "plant_model_v1.pt"
# where labels are stored
LABELS_PATH = ML_DIR / "labels.json"


#model training contrl 
IMAGE_SIZE = 224 # size of images to be used for training
BATCH_SIZE = 32 # number of images to be used in each training batch
EPOCHS = 10 # number of times to train the model on the entire dataset
LEARNING_RATE = 0.0003 # how fast the model learns

def load_labels():
    """Load the labels from the labels.json file."""
    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    
def create_dataloaders():
    """ Changes training images so that the model can understand them better,
    essentially its just simple augmentation (test 1)
    """
    train_transforms = transforms.Compose([
         transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(12),
        transforms.ColorJitter(
            brightness=0.15,
            contrast=0.15,
            saturation=0.15,
        ),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])
    # validation images without changes
    val_transforms = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225],
        ),
    ])
    # trrain images
    train_dataset = datasets.ImageFolder(
        root=TRAIN_DIR,
        transform=train_transforms,
    )
    #validation dataset
    val_dataset = datasets.ImageFolder(
        root=VAL_DIR,
        transform=val_transforms,
    )
    # training image loader
    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=4,
    )
    #validation image loader
    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=4,
    )
    return train_dataset, val_dataset, train_loader, val_loader

