"""
Script 2: Previsión de Lluvia — Clasificación Binaria DNN
==========================================================
Dataset: weather_prediction_dataset.csv (18 ciudades europeas, 2000-2010)
Fuente: https://github.com/florian-huber/weather_prediction_dataset
Predice si lloverá en BASEL el 13/04/2026.
"""

import numpy as np
import pandas as pd
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from logger_config import get_logger

log = get_logger("clasif_lluvia")

CITY = "BASEL"

df = pd.read_csv("weather_prediction_dataset.csv")
data = df[[c for c in df.columns if c.startswith(f"{CITY}_")]].copy()
data.columns = [c.replace(f"{CITY}_", "") for c in data.columns]

data["DATE"] = pd.to_datetime(df.iloc[:, 0], format="%Y%m%d")
data["month"] = data["DATE"].dt.month
data["day"] = data["DATE"].dt.day
doy = data["DATE"].dt.dayofyear
data["sin_day"] = np.sin(2 * np.pi * doy / 365)
data["cos_day"] = np.cos(2 * np.pi * doy / 365)
data["rain"] = (data["precipitation"] > 0).astype(int)

# Se excluye precipitación: usarla como feature sería data leakage directo
feature_cols = [c for c in data.columns
                if c not in ["rain", "precipitation", "DATE"]]
data = data.dropna(subset=feature_cols + ["rain"])

X_train, X_test, y_train, y_test = train_test_split(
    data[feature_cols].values, data["rain"].values,
    test_size=0.2, random_state=42, stratify=data["rain"].values
)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

log.info("Ratio lluvia: %.2f%%", y_train.mean() * 100)
log.info("Features (%d): %s", len(feature_cols), feature_cols)
log.info("Train: %d | Test: %d", len(X_train), len(X_test))

# RA 2.c — Sigmoid en salida: mapea a [0,1] → probabilidad de lluvia.
#           Binary crossentropy: penaliza predicciones confiadas pero erróneas.
model = keras.Sequential([
    keras.layers.Input(shape=(X_train_s.shape[1],)),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(1, activation="sigmoid")
], name="DNN_Clasificacion_Lluvia")

# class_weight compensa el desbalanceo: hay más días sin lluvia que con
class_weight = {0: 1.0, 1: np.sum(y_train == 0) / np.sum(y_train == 1)}
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
model.summary()

# RA 2.d
model.fit(
    X_train_s, y_train,
    epochs=200, batch_size=32, validation_split=0.2,
    class_weight=class_weight, verbose=1,
    callbacks=[keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=15, restore_best_weights=True
    )]
)

# RA 2.e — F1 y Recall importan más que Accuracy en clases desbalanceadas
y_pred = (model.predict(X_test_s).flatten() >= 0.5).astype(int)
report = classification_report(y_test, y_pred, target_names=["No llueve", "Llueve"])
cm = confusion_matrix(y_test, y_pred)

log.info("Reporte de clasificación:\n%s", report)
log.info("Matriz de confusión:\n%s", cm)

# Predicción 13/04/2026 con medias históricas de abril
april_data = data[data["month"] == 4]
april_means = april_data[feature_cols].mean()
april_means.update({"month": 4, "day": 13,
                    "sin_day": np.sin(2 * np.pi * 103 / 365),
                    "cos_day": np.cos(2 * np.pi * 103 / 365)})

prob = model.predict(scaler.transform(april_means.values.reshape(1, -1))).flatten()[0]

log.info("Predicción %s 13/04/2026: %s (P=%.2f%%)",
         CITY, "SÍ LLOVERÁ" if prob >= 0.5 else "NO LLOVERÁ", prob * 100)
log.info("Tasa histórica lluvia abril: %.2f%%", april_data["rain"].mean() * 100)