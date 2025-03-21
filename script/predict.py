from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np

# Charger le modèle pré-entraîné
model = load_model('model/model_wildlens.h5')

# Charger les noms des classes depuis le fichier 'class_names.txt'
with open('class_names.txt', 'r') as f:
    class_names = [line.strip() for line in f.readlines()]

# Fonction pour prédire l'image
def predict_image(img_path):
    # Charger l'image et la redimensionner
    img = image.load_img(img_path, target_size=(150, 150))
    img_array = image.img_to_array(img) / 255.0  # Normaliser l'image
    img_array = np.expand_dims(img_array, axis=0)  # Ajouter une dimension pour simuler un batch

    # Faire la prédiction
    prediction = model.predict(img_array)
    predicted_class_index = np.argmax(prediction)  # Indice de la classe avec la probabilité la plus élevée

    # Trouver le nom de la classe à partir du mappage des noms
    predicted_class = class_names[predicted_class_index]  # Récupérer le nom de la classe à partir de l'indice

    return predicted_class

# Exemple d'utilisation avec une image
img_path = 'dataset/test/Coyote/Coyote_0001 .jpg'  # Chemin vers l'image à tester
predicted_class = predict_image(img_path)

