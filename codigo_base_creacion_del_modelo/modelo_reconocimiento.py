import cv2
import mediapipe as mp
import joblib
import pandas as pd

#configuracion

ARCHIVO_MODELO = "modelo_lsc.pkl"
UMBRAL_CONFIANZA= 0.75 

# Cargar el paquete
paquete= joblib.load(ARCHIVO_MODELO)

#sacamos los elementos del diccionario 
modelo = paquete["modelo"]
columnas = paquete["columnas"]
clases =paquete["clases"]
configuracion = paquete["configuracion"]
metricas = paquete["metricas"]

print("modelo cargado adecuadamente")
print("\n clases guardadas: {clases}")

print(
    "precision de prueba guardada:"
    f"{metricas['accuracy_test']*100:.2f}%"
)
	
#configuracion mediapipe
mp_hands = mp.solutions.hands
mp_drawing=mp.solutions.drawing_utils

estilo_puntos = {
    0: mp_drawing.DrawingSpec(color=(255, 255, 255,), thickness=2, circle_radius=2), #muñeca blanca

   # dedo pulgar 
    1: mp_drawing.DrawingSpec(color=(0  , 0  , 255,), thickness=5, circle_radius=2), #1-4 son pulgar rojo
    2: mp_drawing.DrawingSpec(color=(0  , 0  , 255,), thickness=5, circle_radius=2), #1-4 son pulgar rojo
    3: mp_drawing.DrawingSpec(color=(0  , 0  , 255,), thickness=5, circle_radius=2), #1-4 son pulgar rojo
    4: mp_drawing.DrawingSpec(color=(0  , 0  , 255,), thickness=5, circle_radius=2), #1-4 son pulgar rojo
    
    #dedo indice 
    5: mp_drawing.DrawingSpec(color=(0  , 255 , 0,), thickness=5, circle_radius=2), #5-8 son indice verde
    6: mp_drawing.DrawingSpec(color=(0  , 255 , 0,), thickness=5, circle_radius=2), #5-8 son indice verde
    7: mp_drawing.DrawingSpec(color=(0  , 255 , 0,), thickness=5, circle_radius=2), #5-8 son indice verde
    8: mp_drawing.DrawingSpec(color=(0  , 255 , 0,), thickness=5, circle_radius=2), #5-8 son indice verde

    #dedo medio 
    9: mp_drawing.DrawingSpec(color=(0  , 255 , 255,), thickness=5, circle_radius=2), #9-12 son dedo del medio amarillo
    10: mp_drawing.DrawingSpec(color=(0  , 255 , 255,), thickness=5, circle_radius=2), #9-12 son dedo del medio amarillo
    11: mp_drawing.DrawingSpec(color=(0  , 255 , 255,), thickness=5, circle_radius=2), #9-12 son dedo del medio amarillo
    12: mp_drawing.DrawingSpec(color=(0  , 255 , 255,), thickness=5, circle_radius=2), #9-12 son dedo del medio amarillo

    # dedo anular
    13: mp_drawing.DrawingSpec(color=(128  , 0 , 128,), thickness=5, circle_radius=2), #13-16 son anular morado
    14: mp_drawing.DrawingSpec(color=(128  , 0 , 128,), thickness=5, circle_radius=2), #13-16 son anular morado
    15: mp_drawing.DrawingSpec(color=(128  , 0 , 128,), thickness=5, circle_radius=2), #13-16 son anular morado
    16: mp_drawing.DrawingSpec(color=(128  , 0 , 128,), thickness=5, circle_radius=2), #13-16 son anular morado

    #dedo meñique
    17: mp_drawing.DrawingSpec(color=(255  , 255 , 0,), thickness=5, circle_radius=2), #17-20 son meñique azul
    18: mp_drawing.DrawingSpec(color=(255  , 255 , 0,), thickness=5, circle_radius=2), #17-20 son meñique azul
    19: mp_drawing.DrawingSpec(color=(255  , 255 , 0,), thickness=5, circle_radius=2), #17-20 son meñique azul
    20: mp_drawing.DrawingSpec(color=(255  , 255 , 0,), thickness=5, circle_radius=2), #17-20 son meñique azul
}

estilo_coneccion = mp_drawing.DrawingSpec(
    color=(0, 0, 0 ),
    thickness=2,
)

hands = mp_hands.Hands(
    static_image_mode= False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
)
		
# abrir camara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("no se pudo abrir la camara")
    hands.close()
    raise SystemExit

#reconocimiento

while True:
    ret, frame = cap.read()
    if not ret:
        print("no se pudo capturar la imagen")
        break

    frame = cv2.flip(frame, 1)

    frame_rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )
    resultado = hands.process(frame_rgb)
		
    if resultado.multi_hand_landmarks:

        hand = resultado.multi_hand_landmarks[0]

        mp_drawing.draw_landmarks(
            image= frame, 
            landmark_list =hand,#[], #hands
            connections=mp_hands.HAND_CONNECTIONS,#[],#mp_hands.HAND_CONNECTIONS
            landmark_drawing_spec =estilo_puntos ,
            connection_drawing_spec= estilo_coneccion
        )
		
        #extraer las cordenadas

        datos = []
        for lm in hand.landmark:
            datos.extend([
                lm.x, 
                lm.y, 
                lm.z
            ])
		
        #crea una fila con las mismas colimnas del entrenamiento 
        datos_df = pd.DataFrame(
            [datos],
            columns=columnas
        )
		
        #calculamos las probabilidades

        probabilidades = modelo.predict_proba(
            datos_df
        )[0]

        #buscar la posicion con mayor probabilidad
        indice_mayor = probabilidades.argmax()

        #obtenemos las pociciones de la clase
        letra_predicha = modelo.classes_[
            indice_mayor
        ]
		
        #obtener confianza

        confianza= probabilidades[
            indice_mayor
        ]

        # aplicar el unbral de confianza
        if confianza>= UMBRAL_CONFIANZA:

            texto_resultado =(
                f"{letra_predicha}"
                f"{confianza * 100:.1f}%"
            )

            color_texto = (0, 255, 0)

        else:

            texto_resultado= (
                f"No seguro"
                f"{confianza*100:.1f}%"
            )

            color_texto=(0, 0, 255)

        cv2.putText(
            frame,
            texto_resultado,
            (30, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            color_texto,
            3
        )

    else:
        cv2.putText(
            frame,
            "no se detecta una mano",
            (30,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 0, 255),
            2
        ) 

    cv2.imshow(
        "Reconocimiento LSC",
        frame
    )
	
    if cv2.waitKey(1) & 0xFF == 27:
        break
  
# cerrar todo 
cap.release()
cv2.destroyAllWindows()
hands.close()