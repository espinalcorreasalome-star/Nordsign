import os
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier 

from sklearn.model_selection import train_test_split 
from sklearn.metrics import (
    accuracy_score, 
    confusion_matrix 
)

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
ARCHIVO_CSV = os.path.join(
    BASE_DIR, 
    "archivos_csv", 
    "data.csv"
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
CANTIDAD_ARBOLES= 250
	
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
    .str.upper()
)

#eliminar las etiqutas que esten vacias
data= data[
    data[COLUMNA_ETIQUETA] !=""
] 
print("\n muestra por clase")
print(
    data[COLUMNA_ETIQUETA]
    .value_counts()
    .sort_index()
)

#mostrar el conteo por clases 
print("\nmuestra por clase")
print(data[COLUMNA_ETIQUETA].value_counts().sort_index())

#separar las entradas de las respuestas

X = data.drop(columns=[COLUMNA_ETIQUETA])
y = data[COLUMNA_ETIQUETA]

print(f"\n caracteristicas usadas:{X.shape[1]}")
print(f"clases encontradas: {y.nunique()}")
if X.shape[1] != 63:
    raise ValueError(
        "El dataset debe tener 63 características.\n"
        f"Características encontradas: {X.shape[1]}"
    )

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
    n_estimators=CANTIDAD_ARBOLES, # cantidad de arboles
    random_state= SEMILLA ,# permite reproducir el resultado
     n_jobs= -1 # utiliza todos los núcleos disponibles
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

#guardar todo en un solo archivo 

paquete_modelo={
    "modelo":modelo,
    "columnas":list( X.columns), # se guaarda el orden exacto de las colimnas
    "clases": list( modelo.classes_), # se guardan las clases literal como esten
    "configuracion":{   # se guarda la configuracion principal
        "n_estimators": CANTIDAD_ARBOLES,
        "test_size": TEST_SIZE,
        "random_state": SEMILLA
    },
    "metricas":{ # guardamos algunos resultados
        "accuracy_test": float( precision)
    }
}

joblib.dump(
    paquete_modelo,
    ARCHIVO_MODELO
)
print(f"\n Modelo guardado como :"
      f"{ARCHIVO_MODELO}(●'◡'●)"
)