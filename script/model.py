# scripts/model.py

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

def create_cnn_model(input_shape, num_classes):
    """
    Crée et compile un modèle CNN pour la classification des traces de pas.
    
    :param input_shape: Tuple représentant la forme des images d'entrée (hauteur, largeur, canaux).
    :param num_classes: Nombre de classes (animaux).
    :return: Le modèle CNN compilé.
    """
    model = Sequential([
        # Première couche convolutionnelle
        Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        MaxPooling2D(2, 2),  # MaxPooling pour réduire la taille de l'image

        # Deuxième couche convolutionnelle
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),

        # Troisième couche convolutionnelle
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),

        # Applatissement des images 2D en un vecteur 1D
        Flatten(),

        # Couche entièrement connectée (Fully Connected)
        Dense(512, activation='relu'),
        Dropout(0.5),  # Dropout pour éviter le surapprentissage (overfitting)

        # Couche de sortie : une neurone par classe (avec activation softmax pour classification multi-classes)
        Dense(num_classes, activation='softmax')
    ])

    # Compiler le modèle
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',  # Pour la classification multi-classes
                  metrics=['accuracy'])
    
    return model
