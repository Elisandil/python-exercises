# Título: Informe Técnico: Modelos de Machine Learning para Clasificación y Regresión

Objetivo: Detección de transacciones fraudulentas y predicción de precios inmobiliarios.

Herramientas: Python, Scikit-learn, Pandas, Matplotlib, Seaborn.
Anexo de ejecución: El desarrollo en código de los modelos descritos en este informe se encuentra en el archivo adjunto ejercicios.ipynb.

Alumno: Antonio Ortega Góngora



# Índice

## Índice

- [Título: Informe Técnico: Modelos de Machine Learning para Clasificación y Regresión](#título-informe-técnico-modelos-de-machine-learning-para-clasificación-y-regresión)
- [Índice](#índice)
  - [Índice](#índice-1)
  - [1. Ejercicio 1: Detección de Fraude de Tarjetas de Crédito (Random Forest)](#1-ejercicio-1-detección-de-fraude-de-tarjetas-de-crédito-random-forest)
    - [1.1 Análisis de Datos y Correlación](#11-análisis-de-datos-y-correlación)
    - [1.2 División de Datos (Train/Test)](#12-división-de-datos-traintest)
    - [1.3 Entrenamiento y Evaluación del Modelo](#13-entrenamiento-y-evaluación-del-modelo)
  - [2. Ejercicio 2: Predicción de Precios de Vivienda en California (SVM)](#2-ejercicio-2-predicción-de-precios-de-vivienda-en-california-svm)
    - [2.1 Análisis de Datos y Correlación](#21-análisis-de-datos-y-correlación)
    - [2.2 División de Datos y Preprocesamiento](#22-división-de-datos-y-preprocesamiento)
    - [2.3 Entrenamiento y Evaluación del Modelo](#23-entrenamiento-y-evaluación-del-modelo)
  - [3. Referencias](#3-referencias)



## 1. Ejercicio 1: Detección de Fraude de Tarjetas de Crédito (Random Forest)

El objetivo de este apartado es clasificar de manera binaria una serie de transacciones bancarias, determinando si son legítimas (Clase 0) o fraudulentas (Clase 1).


### 1.1 Análisis de Datos y Correlación

El dataset está compuesto mayoritariamente por variables numéricas transformadas mediante Análisis de Componentes Principales (PCA), etiquetadas de V1 a V28. Por definición matemática, estas variables son ortogonales entre sí, por lo que la búsqueda de multicolinealidad entre ellas es innecesaria.

El análisis de correlación de Pearson se centró exclusivamente en la relación de estas variables con la variable objetivo (Class). Se observó lo siguiente:

Variables como V17, V14, V12 y V10 presentan una correlación negativa significativa con el fraude.

Variables como V11 y V4 muestran una correlación positiva.

Se estableció un umbral de descarte de correlación absoluta de 0.05. Las variables que no superaron este umbral fueron eliminadas del conjunto de entrenamiento por ser consideradas ruido irrelevante para la separación de clases.


### 1.2 División de Datos (Train/Test)

La característica más crítica de este dataset es su desbalanceo extremo: los fraudes representan únicamente en torno al 0.17% del volumen total de datos.

Para realizar la división en conjuntos de entrenamiento (80%) y prueba (20%), fue imperativo utilizar un muestreo estratificado. Esto asegura que la proporción del 0.17% de anomalías se mantenga rigurosamente en ambos subconjuntos. Una partición aleatoria simple corría el riesgo de generar un conjunto de prueba sin un solo caso de fraude, inutilizando la evaluación.


### 1.3 Entrenamiento y Evaluación del Modelo

Se optó por el algoritmo Random Forest Classifier por su robustez frente a relaciones no lineales y su nula necesidad de escalado previo en los datos de entrada.

Dado el desbalanceo, evaluar el modelo usando la métrica de Accuracy (precisión global) habría sido engañoso (un modelo que predijera "0" siempre, acertaría el 99.8% de las veces). Se priorizó la corrección de este sesgo aplicando pesos balanceados en el algoritmo (class_weight='balanced'), forzando al modelo a penalizar duramente los errores en la clase minoritaria. Las métricas de referencia establecidas para juzgar el éxito son el Recall (exhaustividad) de la clase 1 y el análisis de los Falsos Negativos en la matriz de confusión.



## 2. Ejercicio 2: Predicción de Precios de Vivienda en California (SVM)

El objetivo de este modelo es resolver un problema de regresión para estimar la mediana del valor de la vivienda en distritos de California.

### 2.1 Análisis de Datos y Correlación

A diferencia del conjunto de datos del Ejercicio 1, aquí las variables tienen significado físico e interpretable (ingreso, número de habitaciones, población, latitud). Al ejecutar un mapa de calor de correlación se detectaron dos patrones críticos:

MedInc (Ingreso Medio) es la característica que más influye positivamente en el precio de la vivienda, con un coeficiente de 0.69.

AveRooms (Promedio de Habitaciones) y AveBedrms (Promedio de Dormitorios) presentan una correlación cruzada muy alta (0.85), indicando multicolinealidad. Para simplificar la arquitectura predictiva y evitar la redundancia, se eliminó la variable AveBedrms.

### 2.2 División de Datos y Preprocesamiento

Se utilizó una partición clásica de 80% para entrenamiento y 20% para test. Sin embargo, para adaptar este dataset a un modelo basado en Máquinas de Vectores de Soporte (SVR), se aplicaron dos transformaciones obligatorias:

Submuestreo (Subsampling): SVR tiene una complejidad computacional que escala de forma cuadrática o cúbica ($O(n^3)$). Entrenar la matriz completa de más de 16,000 muestras habría supuesto un cuello de botella inaceptable. El conjunto de entrenamiento se redujo de manera aleatoria a 5,000 muestras representativas para garantizar la convergencia del algoritmo.

Estandarización: SVR es un algoritmo basado en distancias. Variables con magnitudes altas, como la población, aplastarían la importancia de variables con magnitudes bajas, como los ingresos. Se aplicó StandardScaler ajustado únicamente sobre los datos de entrenamiento para prevenir fugas de información.

### 2.3 Entrenamiento y Evaluación del Modelo

El modelo empleado fue un Support Vector Regressor (SVR) con un kernel de Función de Base Radial (RBF) para capturar las interacciones no lineales, como la fuerte influencia geoespacial implícita en la latitud y longitud.

El modelo se evalúa en base a dos métricas sobre el conjunto de test transformado: el Error Cuadrático Medio (MSE) y el Coeficiente de Determinación ($R^2$), respaldados por un gráfico de dispersión de valores reales frente a predichos para detectar desviaciones en el ajuste espacial de los datos.



## 3. Referencias

- Machine Learning Group - ULB. (2018). Credit Card Fraud Detection. Kaggle. Recuperado de: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- Scikit-learn developers. (n.d.). California Housing dataset. Scikit-learn Documentation. Recuperado de: https://www.google.com/search?q=https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html
- Scikit-learn developers. (n.d.). Support Vector Machines (SVM). Scikit-learn Documentation. Recuperado de: https://www.google.com/search?q=https://scikit-learn.org/stable/modules/svm.html
- Scikit-learn developers. (n.d.). Random Forest Classifier. Scikit-learn Documentation. Recuperado de: https://www.google.com/search?q=https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html