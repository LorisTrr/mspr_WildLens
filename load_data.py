import os
import glob
import hashlib
import logging
from PIL import Image, ImageEnhance
import random
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HASHES = set()
OUTPUT_DIR = './dataset'
TRAIN_DIR = os.path.join(OUTPUT_DIR, 'train')
VALIDATION_DIR = os.path.join(OUTPUT_DIR, 'validation')
TEST_DIR = os.path.join(OUTPUT_DIR, 'test')

# Création des répertoires nécessaires
os.makedirs(TRAIN_DIR, exist_ok=True)
os.makedirs(VALIDATION_DIR, exist_ok=True)
os.makedirs(TEST_DIR, exist_ok=True)

CATEGORY_COUNTERS = {}

# Fonction pour obtenir le hash unique d'un fichier
def get_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

# Génération d'un nom de fichier séquentiel pour chaque catégorie et ensemble (train/validation/test)
def get_sequential_filename(category, mode='train'):
    CATEGORY_COUNTERS.setdefault(category, {'train': 1, 'validation': 1, 'test': 1})
    filename = f"{category}_{CATEGORY_COUNTERS[category][mode]:04d}.jpg"
    CATEGORY_COUNTERS[category][mode] += 1
    return filename

# Conversion en niveaux de gris
def convert_to_grayscale(img):
    return img.convert('L')  # Convert to grayscale

# Appliquer des augmentations aléatoires à l'image
def apply_augmentation(img):
    augmentations = [
        lambda img: img.rotate(random.randint(-30, 30)),  # Rotation entre -30 et 30 degrés
        lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),  # Flip horizontal
        lambda img: ImageEnhance.Brightness(img).enhance(random.uniform(0.5, 1.5)),  # Variation de luminosité
        lambda img: ImageEnhance.Contrast(img).enhance(random.uniform(0.5, 1.5)),  # Variation de contraste
    ]
    augmentation = random.choice(augmentations)
    return augmentation(img)

# Fonction pour redimensionner, traiter et séparer les images en train, validation et test
def resize_image(file_path, category, mode='train'):
    try:
        file_hash = get_file_hash(file_path)
        if file_hash in HASHES:
            logging.info(f"Duplicate image skipped: {file_path}")
            return
        HASHES.add(file_hash)

        with Image.open(file_path) as img:
            # Convertir en niveaux de gris
            img = convert_to_grayscale(img)

            # Appliquer une augmentation
            img = apply_augmentation(img)

            # Redimensionner l'image à 224x224
            img = img.resize((224, 224), Image.BICUBIC)

            # Sauvegarde de l'image dans le répertoire approprié (train, validation, test)
            category_dir = os.path.join(
                TRAIN_DIR if mode == 'train' else VALIDATION_DIR if mode == 'validation' else TEST_DIR,
                category
            )
            os.makedirs(category_dir, exist_ok=True)
            output_path = os.path.join(category_dir, get_sequential_filename(category, mode))
            img.save(output_path)
            logging.info(f"Processed and saved to: {output_path}")
    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")

# Séparer les images en ensembles train, validation, test (70/15/15)
def process_images(base_dir, train_ratio=0.7, validation_ratio=0.15):
    for category in os.listdir(base_dir):
        category_path = os.path.join(base_dir, category)
        if os.path.isdir(category_path):
            image_files = glob.glob(os.path.join(category_path, '*.[jp][pn]g'))

            # Mélanger les fichiers pour une séparation aléatoire
            random.shuffle(image_files)

            # Calculer la taille de chaque sous-ensemble
            train_size = int(len(image_files) * train_ratio)
            validation_size = int(len(image_files) * validation_ratio)
            test_size = len(image_files) - train_size - validation_size

            # Séparer les fichiers pour l'entraînement, validation et test
            train_files = image_files[:train_size]
            validation_files = image_files[train_size:train_size + validation_size]
            test_files = image_files[train_size + validation_size:]

            # Traiter les images d'entraînement
            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                executor.map(lambda file: resize_image(file, category, mode='train'), train_files)

            # Traiter les images de validation
            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                executor.map(lambda file: resize_image(file, category, mode='validation'), validation_files)

            # Traiter les images de test
            with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                executor.map(lambda file: resize_image(file, category, mode='test'), test_files)

            logging.info(f"Processed category: {category}")

if __name__ == "__main__":
    base_directory = r'downloaded_data/Mammifères/'
    process_images(base_directory)
