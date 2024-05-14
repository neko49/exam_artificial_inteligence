import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Importation des bibliothèques TensorFlow et Keras
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Charger les données
df = pd.read_csv('air_quality_data.csv')

# Prétraitement des données
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['timestamp'] = df['timestamp'].map(pd.Timestamp.timestamp)
features = ['timestamp', 'pm10', 'no2', 'so2', 'o3', 'co']
df = df.dropna(subset=features)

# Sélectionner les caractéristiques et la cible
X = df[features]
y = df['pm25']

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normaliser les données
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Définir l'architecture du modèle de réseau de neurones
model = Sequential()
model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='linear'))

# Compiler le modèle
model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error', metrics=['mae'])

# Entraîner le modèle
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2, verbose=1)

# Évaluation du modèle
loss, mae = model.evaluate(X_test, y_test)
print(f'Mean Absolute Error: {mae}')

# Faire des prédictions
y_pred = model.predict(X_test)

# Visualiser les résultats
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred)
plt.xlabel('Valeurs réelles de PM2.5')
plt.ylabel('Valeurs prédites de PM2.5')
plt.title('Prédictions de PM2.5 avec TensorFlow et Keras')
plt.show()

# Visualiser l'historique de l'entraînement
plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Historique de l\'entraînement')
plt.legend()
plt.show()
