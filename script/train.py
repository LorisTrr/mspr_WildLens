import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.optimizers import Adam

# Répertoires
train_dir = 'dataset/train'  # Répertoire contenant les images d'entraînement
val_dir = 'dataset/validation'  # Répertoire contenant les images de validation

# Préparation des générateurs de données avec augmentation
train_datagen = ImageDataGenerator(
    rescale=1./255,  # Normalisation des pixels
    rotation_range=40,  # Rotation aléatoire
    width_shift_range=0.2,  # Décalage horizontal
    height_shift_range=0.2,  # Décalage vertical
    shear_range=0.2,  # Cisaillement
    zoom_range=0.2,  # Zoom
    horizontal_flip=True,  # Retourner horizontalement
    fill_mode='nearest'  # Mode de remplissage
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,  # Répertoire des images d'entraînement
    target_size=(150, 150),  # Taille des images redimensionnées
    batch_size=32,
    class_mode='categorical'  # Categorical pour les étiquettes multiples
)

val_generator = val_datagen.flow_from_directory(
    val_dir,  # Répertoire des images de validation
    target_size=(150, 150),
    batch_size=32,
    class_mode='categorical'
)

# Créer le modèle CNN
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(150, 150, 3)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(512, activation='relu'),
    layers.Dense(len(train_generator.class_indices), activation='softmax')  # Nombre de classes dans le dataset
])

# Compiler le modèle
model.compile(
    loss='categorical_crossentropy',
    optimizer=Adam(),
    metrics=['accuracy']
)

# Entraîner le modèle
model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // train_generator.batch_size,
    epochs=20,
    validation_data=val_generator,
    validation_steps=val_generator.samples // val_generator.batch_size
)

# Sauvegarder le modèle
model.save('model/model_wildlens.h5')

# Sauvegarder les noms des classes dans un fichier texte
class_names = list(train_generator.class_indices.keys())  # Récupérer les noms des classes à partir du générateur
with open('class_names.txt', 'w') as f:
    for class_name in class_names:
        f.write(f"{class_name}\n")
