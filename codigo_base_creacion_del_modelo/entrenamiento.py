import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
	
# Cargar datos
data = pd.read_csv('vocales.csv')
		
X = data.drop('letra', axis=1)
y = data['letra']
		
# Separar datos
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
		
# Modelo
modelo = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)
	
# Entrenar
modelo.fit(X_train, y_train)
	
# Evaluar
predicciones = modelo.predict(X_test)
accuracy = accuracy_score(y_test, predicciones)
	
print(f"Precisión del modelo: {accuracy*100:.2f}%")
	
# Guardar modelo
joblib.dump(modelo, 'modelo_vocales_lsc.pkl')
print("Modelo guardado (●'◡'●)")
