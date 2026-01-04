#!/usr/bin/env python
# coding: utf-8

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd
import os
import glob
import random

print(f"TensorFlow version: {tf.__version__}")

IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 10

train_dir = "dataset/train"
val_dir = "dataset/validation"

print("Cargando y balanceando imagenes (undersampling)...")

train_pica_files = glob.glob(os.path.join(train_dir, 'pica', '*.png'))
train_nopica_files = glob.glob(os.path.join(train_dir, 'nopica', '*.png'))
val_pica_files = glob.glob(os.path.join(val_dir, 'pica', '*.png'))
val_nopica_files = glob.glob(os.path.join(val_dir, 'nopica', '*.png'))

print(f"Original train: {len(train_pica_files)} pica, {len(train_nopica_files)} nopica")
print(f"Original val: {len(val_pica_files)} pica, {len(val_nopica_files)} nopica")

print("Aplicando undersampling...")
min_train = min(len(train_pica_files), len(train_nopica_files))
min_val = min(len(val_pica_files), len(val_nopica_files))

train_pica_sample = random.sample(train_pica_files, min_train)
train_nopica_sample = random.sample(train_nopica_files, min_train)
val_pica_sample = random.sample(val_pica_files, min_val)
val_nopica_sample = random.sample(val_nopica_files, min_val)

print(f"Nuevo train: {len(train_pica_sample)} pica, {len(train_nopica_sample)} nopica")
print(f"Nuevo val: {len(val_pica_sample)} pica, {len(val_nopica_sample)} nopica")

train_files = train_pica_sample + train_nopica_sample
train_labels = ['pica'] * len(train_pica_sample) + ['nopica'] * len(train_nopica_sample)
val_files = val_pica_sample + val_nopica_sample
val_labels = ['pica'] * len(val_pica_sample) + ['nopica'] * len(val_nopica_sample)

train_df = pd.DataFrame({'filename': train_files, 'class': train_labels})
val_df = pd.DataFrame({'filename': val_files, 'class': val_labels})

train_df = train_df.sample(frac=1).reset_index(drop=True)
val_df = val_df.sample(frac=1).reset_index(drop=True)

print("Generando datos con augmentación...")

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    height_shift_range=0.15,
    brightness_range=[0.7, 1.3],
)

val_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_dataframe(
    train_df,
    x_col='filename',
    y_col='class',
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=True
)

val_generator = val_datagen.flow_from_dataframe(
    val_df,
    x_col='filename',
    y_col='class',
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    shuffle=False
)

print(f"Clases: {train_generator.class_indices}")
print(f"Train (balanceado): {train_generator.n} imagenes")
print(f"Val (balanceado): {val_generator.n} imagenes")

print("\nModelo CNN Simple:")

model = keras.Sequential([
    layers.Conv2D(16, (3,3), activation='relu', input_shape=(224, 224, 3)),
    layers.MaxPooling2D((2,2)),
    layers.Dropout(0.2),
    layers.Conv2D(32, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),
    layers.Dropout(0.3),
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),
    layers.Dropout(0.4),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.4),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.0001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)
model.summary()

print("\nEntrenando... (con Early Stopping)")

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True,
    verbose=1
)

history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=val_generator,
    callbacks=[early_stop],
    verbose=1
)

model.save('model_pica.keras')
print("\nModelo guardado: 'model_pica.keras'")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
epochs_range = range(len(history.history['accuracy']))

ax1.plot(epochs_range, history.history['accuracy'], label='Train', linewidth=2)
ax1.plot(epochs_range, history.history['val_accuracy'], label='Validation', linewidth=2)
ax1.set_title('Accuracy', fontsize=14)
ax1.set_xlabel('Epoca')
ax1.set_ylabel('Accuracy')
ax1.legend()
ax1.grid(True, alpha=0.3)

ax2.plot(epochs_range, history.history['loss'], label='Train', linewidth=2)
ax2.plot(epochs_range, history.history['val_loss'], label='Validation', linewidth=2)
ax2.set_title('Loss', fontsize=14)
ax2.set_xlabel('Epoca')
ax2.set_ylabel('Loss')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('training_history_pica.png', dpi=150)
print("Graficas guardadas")
plt.show()

best_epoch = np.argmin(history.history['val_loss'])
final_accuracy = history.history['accuracy'][best_epoch]
final_val_accuracy = history.history['val_accuracy'][best_epoch]
final_loss = history.history['loss'][best_epoch]
final_val_loss = history.history['val_loss'][best_epoch]

training_info = {
    'architecture': 'CNN Simple + EarlyStopping',
    'stopped_epoch': int(best_epoch + 1),
    'total_epochs_run': len(history.history['accuracy']),
    'final_accuracy': float(final_accuracy),
    'final_val_accuracy': float(final_val_accuracy),
    'final_loss': float(final_loss),
    'final_val_loss': float(final_val_loss),
    'class_indices': train_generator.class_indices,
    'total_train_images': train_generator.n,
    'total_val_images': val_generator.n
}

with open('training_info_pica.json', 'w') as f:
    json.dump(training_info, f, indent=4)
print("Información de entrenamiento guardada.")

print(f"\nBEST EPOCH: {best_epoch + 1}):")
print(f"  Accuracy (train): {training_info['final_accuracy']*100:.2f}%")
print(f"  Accuracy (val): {training_info['final_val_accuracy']*100:.2f}%")
print(f"  Loss (train): {training_info['final_loss']:.4f}")
print(f"  Loss (val): {training_info['final_val_loss']:.4f}")