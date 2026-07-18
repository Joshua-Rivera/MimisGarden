from pathlib import Path
import random
import shutil


ML_DIR = Path(__file__).resolve().parent
RAW_DIR = ML_DIR / "raw" / "new_plant_diseases"
OUTPUT_DIR = ML_DIR / "data"

MAX_TRAIN_IMAGES_PER_LABEL = 1000
MAX_VAL_IMAGES_PER_LABEL = 1000

random.seed(42)


CLASS_MAPPING = {
    "healthy": [
        "Apple___healthy",
        "Blueberry___healthy",
        "Cherry_(including_sour)___healthy",
        "Corn_(maize)___healthy",
        "Grape___healthy",
        "Peach___healthy",
        "Pepper,_bell___healthy",
        "Potato___healthy",
        "Raspberry___healthy",
        "Soybean___healthy",
        "Strawberry___healthy",
        "Tomato___healthy",
    ],
    "leaf_spots": [
        "Apple___Apple_scab",
        "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
        "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
        "Peach___Bacterial_spot",
        "Pepper,_bell___Bacterial_spot",
        "Tomato___Bacterial_spot",
        "Tomato___Septoria_leaf_spot",
        "Tomato___Target_Spot",
        "Strawberry___Leaf_scorch",
    ],
    "severe_damage": [
        "Apple___Black_rot",
        "Apple___Cedar_apple_rust",
        "Cherry_(including_sour)___Powdery_mildew",
        "Corn_(maize)___Common_rust_",
        "Corn_(maize)___Northern_Leaf_Blight",
        "Grape___Black_rot",
        "Grape___Esca_(Black_Measles)",
        "Potato___Early_blight",
        "Potato___Late_blight",
        "Squash___Powdery_mildew",
        "Tomato___Early_blight",
        "Tomato___Late_blight",
        "Tomato___Leaf_Mold",
        "Tomato___Spider_mites Two-spotted_spider_mite",
    ],
}


def find_split_folder(split_names, required=True):
    print(f"Looking inside: {RAW_DIR}")
    print(f"Raw folder exists: {RAW_DIR.exists()}")

    if not RAW_DIR.exists():
        raise FileNotFoundError(f"RAW_DIR does not exist: {RAW_DIR}")

    for folder in RAW_DIR.rglob("*"):
        if folder.is_dir() and folder.name.lower() in split_names:
            print(f"Found split folder: {folder}")
            return folder

    if required:
        raise FileNotFoundError(f"Could not find split folder for {split_names}")

    return None


def get_images_from_classes(split_folder, class_names):
    image_paths = []

    for class_name in class_names:
        class_folder = split_folder / class_name

        if not class_folder.exists():
            print(f"Missing source folder: {class_folder}")
            continue

        for image_path in class_folder.iterdir():
            if image_path.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
                image_paths.append(image_path)

    return image_paths


def reset_output_folder(split_name, mimi_label):
    target_folder = OUTPUT_DIR / split_name / mimi_label

    if target_folder.exists():
        shutil.rmtree(target_folder)

    target_folder.mkdir(parents=True, exist_ok=True)

    return target_folder


def copy_image_list(images, target_folder, mimi_label):
    for index, image_path in enumerate(images):
        new_name = f"{mimi_label}_{index:05d}{image_path.suffix.lower()}"
        target_path = target_folder / new_name
        shutil.copy2(image_path, target_path)


def copy_images_from_existing_split(split_name, source_split_folder, max_per_label):
    for mimi_label, source_classes in CLASS_MAPPING.items():
        target_folder = reset_output_folder(split_name, mimi_label)

        images = get_images_from_classes(source_split_folder, source_classes)
        random.shuffle(images)

        selected_images = images[:max_per_label]

        print(f"{split_name} / {mimi_label}: copying {len(selected_images)} images")

        copy_image_list(selected_images, target_folder, mimi_label)


def copy_images_by_splitting_train(train_folder):
    for mimi_label, source_classes in CLASS_MAPPING.items():
        train_target_folder = reset_output_folder("train", mimi_label)
        val_target_folder = reset_output_folder("val", mimi_label)

        images = get_images_from_classes(train_folder, source_classes)
        random.shuffle(images)

        val_images = images[:MAX_VAL_IMAGES_PER_LABEL]
        train_images = images[
            MAX_VAL_IMAGES_PER_LABEL:
            MAX_VAL_IMAGES_PER_LABEL + MAX_TRAIN_IMAGES_PER_LABEL
        ]

        print(f"train / {mimi_label}: copying {len(train_images)} images")
        print(f"val / {mimi_label}: copying {len(val_images)} images")

        copy_image_list(train_images, train_target_folder, mimi_label)
        copy_image_list(val_images, val_target_folder, mimi_label)


def main():
    print("Preparing Mimi's Garden dataset...")

    train_folder = find_split_folder({"train"})
    val_folder = find_split_folder({"valid", "val", "validation"}, required=False)

    print(f"Train folder selected: {train_folder}")

    if val_folder is None:
        print("No validation folder found. Creating validation split from train data.")
        copy_images_by_splitting_train(train_folder)
    else:
        print(f"Validation folder selected: {val_folder}")

        copy_images_from_existing_split(
            split_name="train",
            source_split_folder=train_folder,
            max_per_label=MAX_TRAIN_IMAGES_PER_LABEL,
        )

        copy_images_from_existing_split(
            split_name="val",
            source_split_folder=val_folder,
            max_per_label=MAX_VAL_IMAGES_PER_LABEL,
        )

    print("Dataset preparation complete.")


if __name__ == "__main__":
    main()
