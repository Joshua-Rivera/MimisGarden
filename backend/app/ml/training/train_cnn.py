
from pathlib import Path  # ease of use for files
import json # who is json?

import torch
from torch import nn # neural networks :D
from torch.utils.data import DataLoader # optimizing how data is loaded
from torchvision import datasets, transforms # ease of use for training
from sklearn.metrics import accuracy_score, f1_score # quantification of results
from tqdm import tqdm # for loading bars
# main ML folder
ML_DIR = Path(__file__).resolve().parent.parent
# training image storage
TRAIN_DIR = ML_DIR / "ml_data" / "train"
# validation image storage
VAL_DIR = ML_DIR / "ml_data" / "val"

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
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}

def load_labels():
    """Load the labels from the labels.json file."""
    with open(LABELS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_dataset_dir(dataset_dir, split_name):
    """Ensure a dataset split exists and contains at least one image."""
    if not dataset_dir.is_dir():
        raise FileNotFoundError(f"{split_name} directory does not exist: {dataset_dir}")

    image_files = [
        path
        for path in dataset_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    ]
    if not image_files:
        raise ValueError(
            f"No images found in {split_name} directory: {dataset_dir}\n"
            "Add images inside its class folders before starting training."
        )
    
def create_dataloaders():
    """ Changes training images so that the model can understand them better,
    essentially its just simple augmentation (test 1)
    """
    validate_dataset_dir(TRAIN_DIR, "training")
    validate_dataset_dir(VAL_DIR, "validation")

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

class MimiCNN(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        # locates patterns in images
        self.features = nn.Sequential (
            # reads image color and simple patters since it is the first layer
            nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            # identifies stronger patterns in images
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            # identifies leaf shapes, marks, and textures (hopefully)
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            # locates deeper plant-health related patterns (hopefullyx2)
            nn.Conv2d(128, 256, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            # locates even deeper plant-health related patterns (hopefullyx3)
            nn.Conv2d(256, 512, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        
        # turns image pattern into a specific class prediction
        self.classifier = nn.Sequential(
            nn.Flatten(),
            #after pooling, the image is 7x7 pixels, so we need to flatten it to a vector of size 512*7*7
            nn.Linear(512 * 7 * 7, 1024),
            nn.ReLU(),
            #assists in reduciing memorizing, therefore reducing overfitting risk
            nn.Dropout(0.5),
            # provides a score per layer
            nn.Linear(1024, num_classes)
        )
        
    def forward(self, x):
        """Forward pass through the network."""
        x = self.features(x) # send image through the pattern finder
        x = self.classifier(x) # send image through the classifier
        return x
        
def create_model(num_classes):
    """Creates the CNN model."""
    model = MimiCNN(num_classes)
    return model

def train_one_epoch(model, train_loader, loss_function, optimizer, device):
    """Train the model for one epoch."""
    model.train()
    total_loss = 0
    for images, labels in tqdm(train_loader, desc="Training"):
        #moves the images and labels to the device (GPU or CPU) for training if available
        images = images.to(device)
        labels = labels.to(device)
        #clears old learning
        optimizer.zero_grad()
        #predictions from the model
        outputs = model(images)
        # checks how wrong the model is
        loss = loss_function(outputs, labels)
        #calculates how to improve the model
        loss.backward()
        # updates the model
        optimizer.step()
        #adds loss for easy tracking
        total_loss += loss.item()
    return total_loss / len(train_loader)
        
def evaluate(model, val_loader, loss_function, device):
    """Evaluate the model on the validation set."""
    model.eval() # puts model in testing mode
    total_loss = 0
    true_labels = []
    pred_labels = []
    #shuts off training updates
    with torch.no_grad():
        for images, labels in tqdm(val_loader, desc="Validating"):
            #moves the images and labels to the device (GPU or CPU) for training if available
            images = images.to(device)
            labels = labels.to(device)
            #predictions from the model
            outputs = model(images)
            # checks how wrong the model is
            loss = loss_function(outputs, labels)
            # chooses the class with the highest score
            predictions = torch.argmax(outputs, dim=1)
            #adds loss for easy tracking
            total_loss += loss.item()
            # saves real labels and predicted labels
            true_labels.extend(labels.cpu().tolist())
            pred_labels.extend(predictions.cpu().tolist())
    # calculates accuracy and f1 score
    accuracy = accuracy_score(true_labels, pred_labels)
    f1 = f1_score(true_labels, pred_labels, average="weighted")
    return total_loss / len(val_loader), accuracy, f1

def save_model(model, labels, class_to_idx, accuracy, f1):
    """Save the model to the specified path."""
    # saves model and its useful info.
    checkpoint = {
        "model_state_dict": model.state_dict(),
        "labels": labels,
        "class_to_idx": class_to_idx,
        "image_size": IMAGE_SIZE,
        "architecture": "custom_mimi_cnn",
        "model_version": "plant_model_v1",
        "validation_accuracy": accuracy,
        "validation_f1": f1,
    }
    torch.save(checkpoint, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")
    
def main():
    """main function :D """
    # load label classes
    labels = load_labels()
    # load image folders
    train_dataset, val_dataset, train_loader, val_loader = create_dataloaders()
    print("Labels:", labels)
    print("Train classes:", train_dataset.classes)
    print("Validation classes:", val_dataset.classes)
    
    #checks folder names match the labels in labels.json
    if train_dataset.classes != labels:
        raise ValueError(
            "Your train folder names do not match labels.json.\n"
            f"Expected: {labels}\n"
            f"Got: {train_dataset.classes}"
        )
    if val_dataset.classes != labels:
        raise ValueError(
            "Your validation folder names do not match labels.json.\n"
            f"Expected: {labels}\n"
            f"Got: {val_dataset.classes}"
        )
    # uses avilable gpus if possible, otherwise uses cpu
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    #creates cnn instance
    model = create_model(num_classes=len(labels))
    model.to(device)
    # indicates the model how to measure mistakes
    loss_function = nn.CrossEntropyLoss()
    # indicates the model how to improve itself
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=LEARNING_RATE
    )
    best_f1_score = 0.0
    for epoch in range(EPOCHS):
        print(f"\nEpoch {epoch + 1}/{EPOCHS}")
        # trains the model for one epoch
        train_loss = train_one_epoch(
            model = model,
            train_loader = train_loader,
            loss_function = loss_function,
            optimizer = optimizer,
            device = device
        )
        # tests the model on testing data
        val_loss, accuracy, f1 = evaluate(
            model = model,
            val_loader = val_loader,
            loss_function = loss_function,
            device = device
        )
        print(f"Train loss: {train_loss:.4f}")
        print(f"Val loss: {val_loss:.4f}")
        print(f"Val accuracy: {accuracy:.4f}")
        print(f"Val F1: {f1:.4f}")

        # saves the best model so far
        if f1 > best_f1_score:
            best_f1_score = f1
            save_model(
                model = model,
                labels = labels,
                class_to_idx = train_dataset.class_to_idx,
                accuracy = accuracy,
                f1 = f1
            )
    print("\nTraining Complete.\n"
          f"Best F1 score: {best_f1_score:.4f}")
if __name__ == "__main__":
    main()
