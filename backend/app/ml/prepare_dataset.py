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

    "yellowing": [
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "Orange___Haunglongbing_(Citrus_greening)",
        "Tomato___Tomato_mosaic_virus",
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
def find_split_folder(split_names):
    candidates = []
    for folder in RAW_DIR.rglob("*"):
        if folder.is_dir() and folder.name.islower() in split_names:
            class_folders = [item for item in folder.iterdir() if item.is_dir()]
            candidates.append((len(class_folders), folder))
    if not candidates:
        raise FileNotFoundError(f"Could not find split folder for {split_names}")
    candidates.sort(reverse=True)
    return candidates[0][1]

def get_images_from_classes(split_folder, class_names):
    image_paths = []
    for class_name in class_names:
        class_folder = split_folder / class_name
        if not class_folder.exists():
            print(f"WARNING: Missing folder - {class_folder}")
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

def copy_images(split_name, source_split_folder, max_per_label):
    for mimi_label, source_classes in CLASS_MAPPING.items():
        target_folder = reset_output_folder(split_name, mimi_label)

        images = get_images_from_classes(source_split_folder, source_classes)
        random.shuffle(images)

        selected_images = images[:max_per_label]

        print(f"{split_name} / {mimi_label}: copying {len(selected_images)} images")

        for index, image_path in enumerate(selected_images):
            new_name = f"{mimi_label}_{index:05d}{image_path.suffix.lower()}"
            target_path = target_folder / new_name
            shutil.copy2(image_path, target_path)

def main():
    train_folder = find_split_folder({"train"})
    val_folder = find_split_folder({"valid", "val", "validation"})

    print(f"Train folder: {train_folder}")
    print(f"Validation folder: {val_folder}")

    copy_images("train", train_folder, MAX_TRAIN_IMAGES_PER_LABEL)
    copy_images("val", val_folder, MAX_VAL_IMAGES_PER_LABEL)

    print("Dataset preparation complete.")


if __name__ == "__main__":
    main()