# train_model.py propre avec MLflow et matrice de confusion (sans data augmentation)

import os
import json
import mlflow
import mlflow.tensorflow
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from model import create_model  # Modifie si tu changes le chemin

# === Paramètres ===
input_shape = (224, 224, 3)
batch_size = 32
epochs = 30
initial_learning_rate = 0.0001
dataset_dir = 'data/processed_balanced'
model_dir = 'model'
os.makedirs(model_dir, exist_ok=True)

# === Chargement des données (sans data augmentation) ===
def load_data(dataset_dir, batch_size, input_shape):
    train_dir = os.path.join(dataset_dir, 'train')
    val_dir = os.path.join(dataset_dir, 'val')
    test_dir = os.path.join(dataset_dir, 'test')

    # === Data augmentation pour l'entraînement ===
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    # Pas d'augmentation pour validation et test
    test_val_datagen = ImageDataGenerator(rescale=1./255)

    train_gen = train_datagen.flow_from_directory(
        train_dir,
        target_size=input_shape[:2],
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=True
    )

    val_gen = test_val_datagen.flow_from_directory(
        val_dir,
        target_size=input_shape[:2],
        batch_size=batch_size,
        class_mode='categorical'
    )

    test_gen = test_val_datagen.flow_from_directory(
        test_dir,
        target_size=input_shape[:2],
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )

    num_classes = len(train_gen.class_indices)
    class_names = list(train_gen.class_indices.keys())
    with open(os.path.join(model_dir, 'class_names.json'), 'w') as f:
        json.dump(class_names, f)

    return train_gen, val_gen, test_gen, num_classes, class_names

# === Visualisation des performances ===
def plot_history(history):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.plot(history.history['accuracy'], label='Train Accuracy')
    ax1.plot(history.history['val_accuracy'], label='Val Accuracy')
    ax1.set_title('Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()

    ax2.plot(history.history['loss'], label='Train Loss')
    ax2.plot(history.history['val_loss'], label='Val Loss')
    ax2.set_title('Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()

    fig.tight_layout()
    curve_path = os.path.join(model_dir, "training_curves.png")
    fig.savefig(curve_path)
    plt.close(fig)
    return curve_path

# === Script principal ===
def main():
    mlflow.set_experiment("Wildlens_Classification")
    with mlflow.start_run(run_name="MobileNetV2_TransferLearning"):
        train_gen, val_gen, test_gen, num_classes, class_names = load_data(dataset_dir, batch_size, input_shape)
        model = create_model(num_classes=num_classes)

        checkpoint = ModelCheckpoint(os.path.join(model_dir, 'wildlens_best_model.h5'), save_best_only=True, monitor='val_accuracy', mode='max', verbose=1)
        early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True, verbose=1)
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-5, verbose=1)

        steps_per_epoch = max(1, train_gen.samples // batch_size)
        val_steps = max(1, val_gen.samples // batch_size)

        history = model.fit(
            train_gen,
            steps_per_epoch=steps_per_epoch,
            validation_data=val_gen,
            validation_steps=val_steps,
            epochs=epochs,
            callbacks=[checkpoint, early_stop, reduce_lr],
            verbose=1
        )

        # Log des métriques
        for epoch in range(len(history.history['loss'])):
            mlflow.log_metric("loss", history.history['loss'][epoch], step=epoch)
            mlflow.log_metric("val_loss", history.history['val_loss'][epoch], step=epoch)
            mlflow.log_metric("accuracy", history.history['accuracy'][epoch], step=epoch)
            mlflow.log_metric("val_accuracy", history.history['val_accuracy'][epoch], step=epoch)

        mlflow.keras.log_model(model, "wildlens_model")
        final_model_path = os.path.join(model_dir, "model_trained.h5")
        model.save(final_model_path)
        mlflow.log_artifact(final_model_path)
        print("Modèle final sauvegardé.")

        # Courbes d'entraînement
        curve_path = plot_history(history)
        mlflow.log_artifact(curve_path)

        # Matrice de confusion
        y_true = test_gen.classes
        y_pred_probs = model.predict(test_gen, verbose=0)
        y_pred = tf.argmax(y_pred_probs, axis=1).numpy()

        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
        plt.title('Matrice de Confusion (Test)')
        plt.xlabel('Prédictions')
        plt.ylabel('Réelles')
        plt.tight_layout()
        confusion_path = os.path.join(model_dir, "confusion_matrix.png")
        plt.savefig(confusion_path)
        plt.close()
        mlflow.log_artifact(confusion_path)
        print("Matrice de confusion enregistrée et loggée dans MLflow")

        print(" Rapport de classification :")
        print(classification_report(y_true, y_pred, target_names=class_names))

if __name__ == "__main__":
    main()
