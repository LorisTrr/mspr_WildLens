import os
import random
import shutil
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array, array_to_img
from PIL import Image

# 📌 PARAMÈTRES
DATA_DIR = "data/downloaded_data/Mammifères"
TARGET_PER_CLASS = 300  # Total par classe après augmentation
SPLIT_RATIOS = {"train": 0.7, "val": 0.15, "test": 0.15}
OUTPUT_DIR = "data/processed_balanced"

# Créer les dossiers de sortie
for split in SPLIT_RATIOS:
    os.makedirs(os.path.join(OUTPUT_DIR, split), exist_ok=True)

# ⚙️ FONCTIONS D'AUGMENTATION
def augment_image(img):
    img = tf.image.random_flip_left_right(img)
    img = tf.image.random_brightness(img, max_delta=0.2)
    img = tf.image.random_contrast(img, lower=0.7, upper=1.3)
    if tf.random.uniform([]) > 0.5:
        img = tf.image.rgb_to_grayscale(img)
        img = tf.image.grayscale_to_rgb(img)
    img = tf.clip_by_value(img, 0.0, 255.0)
    return img

# 🔁 Boucle sur chaque classe
for class_name in os.listdir(DATA_DIR):
    class_path = os.path.join(DATA_DIR, class_name)
    if not os.path.isdir(class_path):
        continue

    print(f"📂 Traitement de la classe : {class_name}")

    # Charger les images originales
    images = [os.path.join(class_path, f) for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
    original_count = len(images)
    target = TARGET_PER_CLASS

    # Charger les images dans un tableau numpy
    loaded_images = []
    for img_path in images:
        try:
            img = load_img(img_path, target_size=(224, 224))
            img_array = img_to_array(img)
            loaded_images.append(img_array)
        except Exception as e:
            print(f"❌ Erreur avec {img_path} : {e}")

    # Créer des images augmentées jusqu'à atteindre TARGET_PER_CLASS
    all_images = loaded_images.copy()
    while len(all_images) < target:
        img = random.choice(loaded_images)
        augmented = augment_image(img)
        all_images.append(augmented.numpy())

    # Mélanger et splitter
    random.shuffle(all_images)
    n_train = int(target * SPLIT_RATIOS["train"])
    n_val = int(target * SPLIT_RATIOS["val"])
    n_test = target - n_train - n_val

    splits = {
        "train": all_images[:n_train],
        "val": all_images[n_train:n_train + n_val],
        "test": all_images[n_train + n_val:]
    }

    # Enregistrement
    for split_name, split_images in splits.items():
        split_dir = os.path.join(OUTPUT_DIR, split_name, class_name)
        os.makedirs(split_dir, exist_ok=True)

        for i, img_array in enumerate(split_images):
            img = array_to_img(img_array)
            img.save(os.path.join(split_dir, f"{class_name}_{i:04d}.jpg"))

print("✅ Tous les fichiers sont équilibrés et enregistrés par classe et par split !")
