"""Train EfficientNet-B0 on the existing Mimi's Garden ImageFolder splits."""

from pathlib import Path
import json
import argparse

import torch
from torch import nn  # neural networks :D
from torch.utils.data import DataLoader  # optimizing how data is loaded
from torchvision import datasets, transforms
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights
from sklearn.metrics import accuracy_score, f1_score  # quantification of results
from tqdm import tqdm  # for loading bars


def getDevice() -> torch.device:
    if torch.cuda.is_available():
        torch.backends.cudnn.benchmark = True
        torch.set_float32_matmul_precision("high")
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


# main ML folder
ML_DIR = Path(__file__).resolve().parent.parent
# training image storage
TRAIN_DIR = ML_DIR / "data" / "train"
# validation image storage
VAL_DIR = ML_DIR / "data" / "val"

# where trained models are saved :D
MODELS_DIR = ML_DIR / "models"
# model file name
MODEL_PATH = MODELS_DIR / "plant_model_v1.pt"
# where labels are stored
LABELS_PATH = ML_DIR / "labels.json"


# model training control area
IMAGE_SIZE = 224  # size of images to be used for training
BATCH_SIZE = 32  # number of images to be used in each training batch
EPOCHS = 10  # number of times to train the model on the entire dataset
LEARNING_RATE = 0.0005  # how fast the model learns
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}
WARMUP_EPOCHS = 2
FINETUNE_LEARNING_RATE = 0.00005
WEIGHTS = EfficientNet_B0_Weights.IMAGENET1K_V1
NUM_WORKERS = 0  # portable default; increase for dedicated training hosts
PATIENCE = 5  # number of epochs to wait for improvement before stopping training


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


def create_dataloaders(manifest_path=None):
    """Changes training images so that the model can understand them better,
    essentially its just simple augmentation (test 1)
    """
    validate_dataset_dir(TRAIN_DIR, "training")
    validate_dataset_dir(VAL_DIR, "validation")

    train_transforms = transforms.Compose(
        [
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
        ]
    )
    # validation images without changes
    val_transforms = WEIGHTS.transforms()
    # training images
    train_dataset = datasets.ImageFolder(
        root=TRAIN_DIR,
        transform=train_transforms,
    )
    # validation dataset
    val_dataset = datasets.ImageFolder(
        root=VAL_DIR,
        transform=val_transforms,
    )
    if manifest_path is not None:
        manifest = json.loads(Path(manifest_path).read_text())
        for dataset, split in ((train_dataset, "train"), (val_dataset, "val")):
            allowed = {str((ML_DIR / name).resolve()) for name in manifest[split]}
            selected = [(path, target) for path, target in dataset.samples if str(Path(path).resolve()) in allowed]
            if len(selected) != len(allowed) or not selected:
                raise ValueError(f"Manifest {split} is empty or refers to missing images")
            dataset.samples = selected
            dataset.imgs = selected
            dataset.targets = [target for _, target in selected]
    # training image loader
    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=torch.cuda.is_available(),
        persistent_workers=NUM_WORKERS > 0,
    )
    # validation image loader
    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=torch.cuda.is_available(),
        persistent_workers=NUM_WORKERS > 0,
    )
    return train_dataset, val_dataset, train_loader, val_loader


def create_model(num_classes, pretrained=True):
    """ImageNet features with a new head returning one logit per project label.

    pretrained=False is for offline smoke tests or reconstructing a checkpoint.
    """
    model = efficientnet_b0(weights=WEIGHTS if pretrained else None)
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
    set_fine_tuning(model, False)
    return model


def set_fine_tuning(model, enabled):
    """Warm up only the classifier, then unfreeze the entire backbone."""
    model.features.requires_grad_(enabled)


def train_one_epoch(model, train_loader, loss_function, optimizer, device, scaler):
    """Train the model for one epoch."""
    model.train()
    if not any(p.requires_grad for p in model.features.parameters()):
        # Frozen BatchNorm statistics and stochastic depth must stay fixed too.
        model.features.eval()
    total_loss = 0
    total_samples = 0
    for images, labels in tqdm(train_loader, desc="Training"):
        # moves the images and labels to the device (GPU or CPU) for training if available
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)

        optimizer.zero_grad(set_to_none=True)

        with torch.amp.autocast(device_type=device.type, enabled=device.type == "cuda"):
            outputs = model(images)
            loss = loss_function(outputs, labels)

        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        # adds loss for easy tracking
        total_loss += loss.item() * labels.size(0)
        total_samples += labels.size(0)
    return total_loss / total_samples


def evaluate(model, val_loader, loss_function, device):
    """Evaluate the model on the validation set."""
    model.eval()  # puts model in testing mode
    total_loss = 0
    total_samples = 0
    true_labels = []
    pred_labels = []
    # shuts off training updates
    with torch.no_grad():
        for images, labels in tqdm(val_loader, desc="Validating"):
            # moves the images and labels to the device (GPU or CPU) for training if available
            images = images.to(device, non_blocking=True)
            labels = labels.to(device, non_blocking=True)
            # predictions from the model
            with torch.amp.autocast(
                device_type=device.type, enabled=device.type == "cuda"
            ):
                outputs = model(images)
                # checks how wrong the model is
                loss = loss_function(outputs, labels)
            # chooses the class with the highest score
            predictions = torch.argmax(outputs, dim=1)
            # adds loss for easy tracking
            total_loss += loss.item() * labels.size(0)
            total_samples += labels.size(0)
            # saves real labels and predicted labels
            true_labels.extend(labels.cpu().tolist())
            pred_labels.extend(predictions.cpu().tolist())
    # calculates accuracy and f1 score
    accuracy = accuracy_score(true_labels, pred_labels)
    f1 = f1_score(true_labels, pred_labels, average="weighted", zero_division=0)
    return total_loss / total_samples, accuracy, f1


def save_model(model, labels, class_to_idx, accuracy, f1, epoch, optimizer, scaler, val_loss):
    """Save the model to the specified path."""
    # saves model and its useful info.
    checkpoint = {
        "model_state_dict": model.state_dict(),
        "labels": labels,
        "class_to_idx": class_to_idx,
        "image_size": IMAGE_SIZE,
        "architecture": "efficientnet_b0",
        "pretrained_weights": WEIGHTS.name,
        "preprocessing": {
            "resize_size": 256, "crop_size": IMAGE_SIZE, "interpolation": "bicubic",
            "mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225],
        },
        "epoch": epoch,
        "optimizer_state_dict": optimizer.state_dict(),
        "scaler_state_dict": scaler.state_dict(),
        "validation_loss": val_loss,
        "model_version": "plant_model_v1",
        "training_config": {"warmup_epochs": WARMUP_EPOCHS, "head_lr": LEARNING_RATE, "backbone_lr": FINETUNE_LEARNING_RATE, "batch_size": BATCH_SIZE, "seed": 42},
        "validation_accuracy": accuracy,
        "validation_f1": f1,
    }
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    temporary_path = MODEL_PATH.with_suffix(".pt.tmp")
    torch.save(checkpoint, temporary_path)
    temporary_path.replace(MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")


def main():
    """Warm up the head, fine-tune, and retain the best validation checkpoint."""
    global EPOCHS, WARMUP_EPOCHS, BATCH_SIZE, NUM_WORKERS
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=int, default=EPOCHS)
    parser.add_argument("--warmup-epochs", type=int, default=WARMUP_EPOCHS)
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument("--workers", type=int, default=NUM_WORKERS)
    parser.add_argument("--manifest", type=Path, default=ML_DIR / "reports/splits.json")
    args = parser.parse_args()
    if args.epochs < 1 or not 0 <= args.warmup_epochs < args.epochs or args.batch_size < 2 or args.workers < 0:
        parser.error("Use epochs > warmup >= 0, batch-size >= 2, and workers >= 0")
    EPOCHS, WARMUP_EPOCHS, BATCH_SIZE, NUM_WORKERS = args.epochs, args.warmup_epochs, args.batch_size, args.workers
    torch.set_num_threads(4)
    torch.manual_seed(42)
    # load label classes
    labels = load_labels()
    # load image folders
    train_dataset, val_dataset, train_loader, val_loader = create_dataloaders(args.manifest)
    print("Labels:", labels)
    print("Train classes:", train_dataset.classes)
    print("Validation classes:", val_dataset.classes)

    # checks folder names match the labels in labels.json
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
    device = getDevice()
    print(f"Using device: {device}")

    # creates cnn instance
    model = create_model(num_classes=len(labels))
    model.to(device)
    # indicates the model how to measure mistakes
    loss_function = nn.CrossEntropyLoss()
    # indicates the model how to improve itself
    optimizer = torch.optim.AdamW([
        {"params": model.classifier.parameters(), "lr": LEARNING_RATE},
        {"params": model.features.parameters(), "lr": FINETUNE_LEARNING_RATE},
    ], weight_decay=0.0001)
    scaler = torch.amp.GradScaler("cuda", enabled=device.type == "cuda")
    best_f1_score = -1.0
    epochs_without_improvement = 0
    history = []
    for epoch in range(EPOCHS):
        if epoch == WARMUP_EPOCHS:
            set_fine_tuning(model, True)
            print("Fine-tuning all features with a lower backbone learning rate.")
        print(f"\nEpoch {epoch + 1}/{EPOCHS}")
        # trains the model for one epoch
        train_loss = train_one_epoch(
            model=model,
            train_loader=train_loader,
            loss_function=loss_function,
            optimizer=optimizer,
            device=device,
            scaler=scaler,
        )
        # Evaluate only the validation split.
        val_loss, accuracy, f1 = evaluate(
            model=model,
            val_loader=val_loader,
            loss_function=loss_function,
            device=device,
        )
        print(f"Train loss: {train_loss:.4f}")
        print(f"Val loss: {val_loss:.4f}")
        print(f"Val accuracy: {accuracy:.4f}")
        print(f"Val F1: {f1:.4f}")

        history.append({"epoch": epoch + 1, "train_loss": train_loss, "validation_loss": val_loss, "validation_accuracy": accuracy, "validation_f1": f1})
        report_dir = ML_DIR / "reports"
        report_dir.mkdir(exist_ok=True)
        (report_dir / "training_history.json").write_text(json.dumps(history, indent=2))
        # saves the best model so far
        if f1 > best_f1_score:
            best_f1_score = f1
            epochs_without_improvement = 0
            save_model(
                model=model,
                labels=labels,
                class_to_idx=train_dataset.class_to_idx,
                accuracy=accuracy,
                f1=f1,
                epoch=epoch + 1,
                optimizer=optimizer,
                scaler=scaler,
                val_loss=val_loss,
            )
        elif f1 <= best_f1_score:
            epochs_without_improvement += 1
            print(f"No improvement in Epoch: {epoch + 1}")
            if epochs_without_improvement >= PATIENCE:
                print(
                    "No improvement for several epochs. Early Stopping, training ended."
                )
                break
    print("\nTraining Complete.\n" f"Best F1 score: {best_f1_score:.4f}")


if __name__ == "__main__":
    main()
