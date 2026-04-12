"""
Script 1: Estimación Térmica — Regresión DNN
=============================================
Dataset: weather_prediction_dataset.csv (18 ciudades europeas, 2000-2010)
Fuente: https://github.com/florian-huber/weather_prediction_dataset
Predice temperatura media diaria en BASEL para el 13/04/2026.
"""

import numpy as np
import pandas as pd
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from logger_config import get_logger

log = get_logger("regresion_temp")

CITY = "BASEL"
TARGET = "temp_mean"

df = pd.read_csv("weather_prediction_dataset.csv")
data = df[[c for c in df.columns if c.startswith(f"{CITY}_")]].copy()
data.columns = [c.replace(f"{CITY}_", "") for c in data.columns]

data["DATE"] = pd.to_datetime(df.iloc[:, 0], format="%Y%m%d")
data["month"] = data["DATE"].dt.month
data["day"] = data["DATE"].dt.day
doy = data["DATE"].dt.dayofyear
# Encoding cíclico: evita que el modelo interprete dic→ene como salto discontinuo
data["sin_day"] = np.sin(2 * np.pi * doy / 365)
data["cos_day"] = np.cos(2 * np.pi * doy / 365)

feature_cols = [c for c in data.columns if c not in [TARGET, "DATE"]]
data = data.dropna(subset=feature_cols + [TARGET])

X_train, X_test, y_train, y_test = train_test_split(
    data[feature_cols].values, data[TARGET].values,
    test_size=0.2, random_state=42
)

scaler_X, scaler_y = StandardScaler(), StandardScaler()
X_train_s = scaler_X.fit_transform(X_train)
X_test_s = scaler_X.transform(X_test)
y_train_s = scaler_y.fit_transform(y_train.reshape(-1, 1)).flatten()

log.info("Features (%d): %s", len(feature_cols), feature_cols)
log.info("Train: %d | Test: %d", len(X_train), len(X_test))

# RA 2.c — Lineal en salida: la temperatura no tiene rango acotado.
#           MSE como loss: penaliza errores grandes cuadráticamente.
model = keras.Sequential([
    keras.layers.Input(shape=(X_train_s.shape[1],)),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dense(1, activation="linear")
], name="DNN_Regresion_Temperatura")

model.compile(optimizer="adam", loss="mse", metrics=["mae"])
model.summary()

# RA 2.d
model.fit(
    X_train_s, y_train_s,
    epochs=200, batch_size=32, validation_split=0.2, verbose=1,
    callbacks=[keras.callbacks.EarlyStopping(
        monitor="val_loss", patience=15, restore_best_weights=True
    )]
)

# RA 2.e — Métricas en escala original (°C) tras desnormalizar
y_pred = scaler_y.inverse_transform(
    model.predict(X_test_s).reshape(-1, 1)
).flatten()

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

log.info("MAE:  %.2f °C", mae)
log.info("RMSE: %.2f °C", rmse)
log.info("R²:   %.4f", r2)

# Predicción 13/04/2026: medias históricas de abril como proxy
# porque el dataset solo llega a 2010 (extrapolación inevitable).
april_data = data[data["month"] == 4]
april_means = april_data[feature_cols].mean()
april_means.update({"month": 4, "day": 13,
                    "sin_day": np.sin(2 * np.pi * 103 / 365),
                    "cos_day": np.cos(2 * np.pi * 103 / 365)})

pred_temp = scaler_y.inverse_transform(
    model.predict(scaler_X.transform(april_means.values.reshape(1, -1)))
).flatten()[0]

log.info("Predicción %s 13/04/2026: %.2f °C", CITY, pred_temp)
log.info("Media histórica abril: %.2f ± %.2f °C",
         april_data[TARGET].mean(), april_data[TARGET].std())