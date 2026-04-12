"""
Script 3: Localización Geográfica — Clasificación Multiclase DNN
=================================================================
Dataset: weather_prediction_dataset.csv (18 ciudades europeas, 2000-2010)
Fuente: https://github.com/florian-huber/weather_prediction_dataset
Dado (temperatura, humedad, precipitación), predice el PAÍS de la estación.
"""

import numpy as np
import pandas as pd
from tensorflow import keras
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
from logger_config import get_logger

log = get_logger("clasif_pais")

FEATURES = ["temp_mean", "humidity", "precipitation"]

CITY_COUNTRY = {
    "BASEL": "Suiza", "BUDAPEST": "Hungría",
    "DE_BILT": "Países Bajos", "MAASTRICHT": "Países Bajos",
    "DRESDEN": "Alemania", "DUSSELDORF": "Alemania",
    "KASSEL": "Alemania", "MUNCHEN": "Alemania",
    "HEATHROW": "Reino Unido", "LJUBLJANA": "Eslovenia",
    "MALMO": "Suecia", "STOCKHOLM": "Suecia",
    "MONTELIMAR": "Francia", "PERPIGNAN": "Francia", "TOURS": "Francia",
    "OSLO": "Noruega", "ROMA": "Italia", "SONNBLICK": "Austria",
}

df = pd.read_csv("weather_prediction_dataset.csv")

# De formato ancho (1 col/ciudad) a largo (1 fila/día-ciudad)
rows = []
for city, country in CITY_COUNTRY.items():
    cols = {f: f"{city}_{f}" for f in FEATURES}
    if all(c in df.columns for c in cols.values()):
        chunk = df[list(cols.values())].copy()
        chunk.columns = FEATURES
        chunk["country"] = country
        rows.append(chunk)

data = pd.concat(rows, ignore_index=True).dropna()

le = LabelEncoder()
y_encoded = le.fit_transform(data["country"].values)
y_onehot = keras.utils.to_categorical(y_encoded)

log.info("Registros: %d | Clases (%d): %s",
         len(data), len(le.classes_), list(le.classes_))
log.info("Distribución:\n%s", data["country"].value_counts().to_string())

X_train, X_test, y_train, y_test, _, y_enc_test = train_test_split(
    data[FEATURES].values, y_onehot, y_encoded,
    test_size=0.2, random_state=42, stratify=y_encoded
)

scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s = scaler.transform(X_test)

# RA 2.c — Softmax en salida: distribución de probabilidad sobre N países (suma=1).
#           Categorical crossentropy: compara softmax predicho con one-hot real.
#           Red más ancha (256) porque solo 3 features deben discriminar 10 clases.
model = keras.Sequential([
    keras.layers.Input(shape=(len(FEATURES),)),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(256, activation="relu"),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.BatchNormalization(),
    keras.layers.Dropout(0.2),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dense(len(le.classes_), activation="softmax")
], name="DNN_Clasificacion_Pais")

model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.summary()

# RA 2.d — ReduceLROnPlateau baja el lr si val_loss se estanca,
#           útil cuando la superficie de pérdida tiene mesetas.
model.fit(
    X_train_s, y_train,
    epochs=200, batch_size=64, validation_split=0.2, verbose=1,
    callbacks=[
        keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=15, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss", factor=0.5, patience=7, min_lr=1e-6)
    ]
)

# RA 2.e — Accuracy esperada ~30-50%: con solo 3 features,
#           países con clima similar (Alemania/Países Bajos) se confunden.
y_pred = np.argmax(model.predict(X_test_s), axis=1)
report = classification_report(y_enc_test, y_pred, target_names=le.classes_)
cm = confusion_matrix(y_enc_test, y_pred)

log.info("Reporte de clasificación:\n%s", report)
log.info("Matriz de confusión:\n%s", cm)

# Predicción con valores de ejemplo
temp_in, hum_in, prec_in = 12.5, 75.0, 5.0
probs = model.predict(
    scaler.transform(np.array([[temp_in, hum_in, prec_in]]))
).flatten()

log.info("Entrada: temp=%.1f°C, hum=%.1f%%, prec=%.1f", temp_in, hum_in, prec_in)
log.info("País predicho: %s (%.2f%%)", le.classes_[np.argmax(probs)], probs.max() * 100)
for cls, p in sorted(zip(le.classes_, probs), key=lambda x: -x[1]):
    log.info("  %-15s: %5.2f%% %s", cls, p * 100, "█" * int(p * 40))