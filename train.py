# train.py
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from model import create_model

# === Paramètres ===
img_size = (224, 224)
batch_size = 32
epochs = 30

base_dir = "data/processed_balanced"
train_dir = os.path.join(base_dir, "train")
val_dir = os.path.join(base_dir, "val")
test_dir = os.path.join(base_dir, "test")

# === Générateurs ===
datagen = ImageDataGenerator(rescale=1./255)

train_generator = datagen.flow_from_directory(train_dir, target_size=img_size, batch_size=batch_size, class_mode='categorical')
val_generator = datagen.flow_from_directory(val_dir, target_size=img_size, batch_size=batch_size, class_mode='categorical')
test_generator = datagen.flow_from_directory(test_dir, target_size=img_size, batch_size=batch_size, class_mode='categorical', shuffle=False)

# === Infos classes ===
num_classes = len(train_generator.class_indices)
class_names = list(train_generator.class_indices.keys())

print("\n📊 Nombre d’images par classe :")
for name in class_names:
    train_count = len(os.listdir(os.path.join(train_dir, name)))
    val_count = len(os.listdir(os.path.join(val_dir, name)))
    test_count = len(os.listdir(os.path.join(test_dir, name)))
    print(f"🦴 {name:<20} → train: {train_count}, val: {val_count}, test: {test_count}")

# === Création du modèle ===
model = create_model(num_classes)
model.summary()

# === Callbacks ===
early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

# === Entraînement ===
history = model.fit(train_generator, validation_data=val_generator, epochs=epochs, callbacks=[early_stopping])

# === Évaluation finale ===
test_loss, test_acc = model.evaluate(test_generator)
print(f"\n✅ Précision finale sur le test : \033[92m{test_acc * 100:.2f}%\033[0m")

# === Prédictions ===
y_pred = model.predict(test_generator, verbose=1)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = test_generator.classes

# === Matrice de confusion ===
cm = confusion_matrix(y_true, y_pred_classes)
plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
plt.xlabel('Prédictions')
plt.ylabel('Véritables')
plt.title('🔍 Matrice de Confusion')
plt.tight_layout()
plt.show()

# === Rapport de classification ===
print("📝 Rapport de classification :")
print(classification_report(y_true, y_pred_classes, target_names=class_names))

# === Courbes d’entraînement ===
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label="Entraînement")
plt.plot(history.history['val_accuracy'], label="Validation")
plt.title("📈 Précision")
plt.xlabel("Époques")
plt.ylabel("Précision")
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label="Entraînement")
plt.plot(history.history['val_loss'], label="Validation")
plt.title("📉 Perte")
plt.xlabel("Époques")
plt.ylabel("Perte")
plt.legend()

plt.tight_layout()
plt.show()

# === Sauvegarde du modèle ===
model.save("model_trained.h5")
print("\n💾 Modèle sauvegardé dans 'model_trained.h5'")
