import os
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier #

from sklearn.model_selection import (
    train_test_split, #
    cross_val_score, #
    StratifiedKFold, #
)
from sklearn.metrics import (
    accuracy_score, #
    confusion_matrix, #
    classification_report #
)

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
ARCHIVO_CSV = os.path.join(
    BASE_DIR, 
    "archivos_csv", 
    "data.csv"
)

ARCHIVO_LANDMARKS = os.path.join(
    BASE_DIR, 
    "archivos_csv", 
    "importancia_landmarks.csv"
)
ARCHIVO_MATRIZ = os.path.join(
    BASE_DIR, 
    "archivos_csv", 
    "matriz_confusion_lasic.csv"
)


# configuracion 

ARCHIVO_MODELO = os.path.join(BASE_DIR, "modelo_lsc.pkl")
COLUMNA_ETIQUETA = "letra"

TEST_SIZE = 0.20
SEMILLA = 42
	
# Cargar datos

data = pd.read_csv(ARCHIVO_CSV)
print("informacion del dataset")
print(f"\ncantidad total de muestras: {len(data)}" )
print(f"cantidad de columnas: {len(data.columns)}")

# comprobar la columna de etiqueta 

if COLUMNA_ETIQUETA not in data.columns:
    raise ValueError(
        f"no existe la columna {COLUMNA_ETIQUETA}"
        f"las columnas encontradas son: {list(data.columns)}"
    )
#eliminar filas que estan totalmente vacias 
data = data.dropna(how="all")	

#eliminar filas ue no tienen clase 
data= data.dropna(subset=COLUMNA_ETIQUETA)

#convertir las etiquetas en un texto y quitar espacios 
data[COLUMNA_ETIQUETA]=(
    data[COLUMNA_ETIQUETA]
    .astype(str)
    .str.strip()
)

#eliminar las etiqutas que esten vacias
data= data[data[COLUMNA_ETIQUETA] != ""]

#mostrar el conteo por clases 
print("\nmuestra por clase")
print(data[COLUMNA_ETIQUETA].value_counts().sort_index())

#separar las entradas de las respuestas

X = data.drop(columns=[COLUMNA_ETIQUETA])
y = data[COLUMNA_ETIQUETA]

print(f"\n caracteristicas usadas:{X.shape[1]}")
print(f"clases encontradas: {y.nunique()}")

#stratified splitting : esto hace que la divicion de los datos mantenga su proporconalidad
#por ejemplo tienes 50 muestras de A y 30 de B ,esto no dividira su mitad sino su proporcion
#lo puse para que el modelo tenga una evaluacion justa y no sea menos confiable (●'◡'●)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=SEMILLA,
    stratify=y
)


print("\nDivisión del dataset")
print("\n"f"Entrenamiento: {len(X_train)} muestras")
print(f"Prueba: {len(X_test)} muestras")

# creamos random forest 

modelo = RandomForestClassifier(
    n_estimators=300, # cantidad de arboles
    min_samples_split=4, # se necesitan minimo 4 muestras para dividir un nodo
    min_samples_leaf=2, # cada hoja debe conservar al menos 2 muestras
    class_weight="balanced", # intenta compensar clases con distintas cantidades
    n_jobs= -1, # utiliza todos los núcleos disponibles
    random_state= SEMILLA # permite reproducir el resultado
)

# Cross-Validation :evalua que tan generalizado esta el modelo
#evita el overfitting o sobreajute para los q no sabemos ingles :(
#en cristiano,esto asegura que no se memoris elos dtos sino que aprenda los patrones

validacion = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=SEMILLA
)

puntajes_cv = cross_val_score(
    modelo,
    X,
    y,
    cv=validacion,
    scoring="accuracy",
    n_jobs=-1
)

print("\nvalidación cruzada")

for numero, puntaje in enumerate(puntajes_cv, start=1):
    print(f"división {numero}: {puntaje * 100:.2f}%")

print(
    f"promedio: {puntajes_cv.mean() * 100:.2f}%"
)

print(
    f"variación: ±{puntajes_cv.std() * 100:.2f}%"
)

# Entrenar
print("\n entrenamiento del modelo")
modelo.fit(
    X_train, 
    y_train)
	
# Evaluar con las pruebas
predicciones = modelo.predict(X_test)

precision = accuracy_score(
    y_test,
    predicciones
)
	
print(f"\n evaluacion final")
print (f"\n Precision: {precision*100:.2f}%")

# resultados por clase (●'◡'●)
print("\n resultados de clasificacion")

print( classification_report(
          y_test,
          predicciones,
          labels=modelo.classes_,
          zero_division=0
      )
)

# matriz de confucion
# se diferencia del accuracy porque este da porcentajes abiertos y la matriz mide el rendimiento del moelo en clasificcion
# en español,accurracy= porcentaje general/matriz=desclose de predicciones correctas e incorrectas

matriz = confusion_matrix(
    y_test,
    predicciones,
    labels= modelo.classes_
)

matriz_df= pd.DataFrame(
    matriz,
    index=[
        f" Real_{clase}"
        for clase in modelo.classes_
    ],
    columns=[
        f" Pred_{clase}"
        for clase in modelo.classes_
    ]
)
	
print("\n matriz de confusion")
print(matriz_df)

# gualdamos la matrisss
matriz_df.to_csv(
    ARCHIVO_MATRIZ,
    encoding="utf-8"
)

# clases que aprendio :)
print("\n clases aprendidas por el modelo")

for numero,clase in enumerate(
    modelo.classes_,
    start=1
):
    print(f"{numero}. {clase}")

#feature importanci 
# es una tecnica que mide que tanto afecta una variable a la prediccion
#nos sirve para :saber que cosas inluyen en la toma de deciciones y como filtrarlo despues 

importancias= pd.DataFrame({
    "caracteristica": X.columns,
    "importancia": modelo.feature_importances_
})

importancias = importancias.sort_values(
    by="importancia",
    ascending= False
)

print("\n 15 caracteristicas mas importantes")

print(importancias.head(15).to_string(index=  False))

importancias.to_csv(
    ARCHIVO_LANDMARKS,
    index=False,
    encoding="utf-8"
)

#guardar todo en un solo archivo 

paquete_modelo={
    "modelo":modelo,
    "columnas":list( X.columns), # se guaarda el orden exacto de las colimnas
    "clases": list( modelo.classes_), # se guardan las clases literal como esten
    "configuracion":{   # se guarda la configuracion principal
        "n_estimators": 500,
        "min_samples_split":4,
        "min_samples_leaf":2,
        "test_size": TEST_SIZE,
        "random_state": SEMILLA
    },
    "metricas":{ # guardamos algunos resultados
        "accuracy_test": float( precision),
        "cross_validation_mean": float(puntajes_cv.mean()),
        "cross_validation_std": float(puntajes_cv.std())
    }
}

joblib.dump(
    paquete_modelo,
    ARCHIVO_MODELO
)
print(f"\n Modelo guardado como :"
      f"{ARCHIVO_MODELO}(●'◡'●)"
)