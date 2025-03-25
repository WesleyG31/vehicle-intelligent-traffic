import os
import cv2
import shutil
import random
from tqdm import tqdm

# Paths base
ORIG_IMG_PATH = r"C:\Todos mis documentos\vehicle-intelligent-traffic\data\raw_data\images"
ORIG_LBL_PATH = r"C:\Todos mis documentos\vehicle-intelligent-traffic\data\raw_data\labels"

OUT_PATH = r"C:\Todos mis documentos\vehicle-intelligent-traffic\data\ua-detrac"
IMG_OUT = os.path.join(OUT_PATH, "images")
LBL_OUT = os.path.join(OUT_PATH, "labels")

# Create the folders
def create_dirs():
    for split in ["train", "val", "test"]:
        os.makedirs(os.path.join(IMG_OUT, split), exist_ok=True)
        os.makedirs(os.path.join(LBL_OUT, split), exist_ok=True)

# Detect if the image is fuzzy
def is_blurry(image, threshold=100.0):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = cv2.Laplacian(gray, cv2.CV_64F).var()
    return fm < threshold

# resize images 
def process_dataset(split_ratio=(0.7, 0.2, 0.1), resize=(640, 480)):
    create_dirs()

    images = [f for f in os.listdir(ORIG_IMG_PATH) if f.endswith(".jpg")]
    random.shuffle(images)

    total = len(images)
    train_end = int(split_ratio[0] * total)
    val_end = train_end + int(split_ratio[1] * total)

    splits = {
        "train": images[:train_end],
        "val": images[train_end:val_end],
        "test": images[val_end:]
    }

    for split, files in splits.items():
        for img_name in tqdm(files, desc=f"Procesando {split}"):
            img_path = os.path.join(ORIG_IMG_PATH, img_name)
            label_name = img_name.replace(".jpg", ".txt")
            label_path = os.path.join(ORIG_LBL_PATH, label_name)

            if not os.path.exists(label_path):
                continue

            image = cv2.imread(img_path)
            if is_blurry(image):
                continue  # Skip imágenes borrosas

            resized = cv2.resize(image, resize)
            out_img_path = os.path.join(IMG_OUT, split, img_name)
            out_lbl_path = os.path.join(LBL_OUT, split, label_name)

            cv2.imwrite(out_img_path, resized)
            shutil.copyfile(label_path, out_lbl_path)

    print("✅ Dataset preprocesado y organizado con éxito.")

if __name__ == "__main__":
    process_dataset()
