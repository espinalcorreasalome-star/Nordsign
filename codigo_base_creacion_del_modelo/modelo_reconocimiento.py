import os

import cv2
import mediapipe as mp
import joblib
import pandas as pd

from validaciones import(
    es_b_valida,
  #  es_o_valida
)

#configuracion
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

ARCHIVO_MODELO = os.path.join(
    BASE_DIR,
    "modelo_lsc.pkl"
)
#cargamos el modelo

if not os.path.exists(ARCHIVO_MODELO):
    raise FileNotFoundError(
        "no se encontro el modelo.\n"
        f"ruta buscada:\n{ARCHIVO_MODELO}"
    )

paquete= joblib.load(
    ARCHIVO_MODELO
)

if not isinstance(paquete, dict):
    raise TypeError(
        "El archivo cargado no contiene "
        "el paquete del modelo esperado."
    )

#sacamos los elementos del diccionario 
modelo = paquete["modelo"]
columnas = paquete["columnas"]

#configuracion mediapipe
mp_hands = mp.solutions.hands
mp_drawing=mp.solutions.drawing_utils

estilo_puntos = {
     # Muñeca: blanco
    0: mp_drawing.DrawingSpec(
        color=(255, 255, 255),
        thickness=2,
        circle_radius=2
    ),

    # Pulgar: rojo
    1: mp_drawing.DrawingSpec(
        color=(0, 0, 255),
        thickness=5,
        circle_radius=2
    ),
    2: mp_drawing.DrawingSpec(
        color=(0, 0, 255),
        thickness=5,
        circle_radius=2
    ),
    3: mp_drawing.DrawingSpec(
        color=(0, 0, 255),
        thickness=5,
        circle_radius=2
    ),
    4: mp_drawing.DrawingSpec(
        color=(0, 0, 255),
        thickness=5,
        circle_radius=2
    ),

    # Índice: verde
    5: mp_drawing.DrawingSpec(
        color=(0, 255, 0),
        thickness=5,
        circle_radius=2
    ),
    6: mp_drawing.DrawingSpec(
        color=(0, 255, 0),
        thickness=5,
        circle_radius=2
    ),
    7: mp_drawing.DrawingSpec(
        color=(0, 255, 0),
        thickness=5,
        circle_radius=2
    ),
    8: mp_drawing.DrawingSpec(
        color=(0, 255, 0),
        thickness=5,
        circle_radius=2
    ),

    # Medio: amarillo
    9: mp_drawing.DrawingSpec(
        color=(0, 255, 255),
        thickness=5,
        circle_radius=2
    ),
    10: mp_drawing.DrawingSpec(
        color=(0, 255, 255),
        thickness=5,
        circle_radius=2
    ),
    11: mp_drawing.DrawingSpec(
        color=(0, 255, 255),
        thickness=5,
        circle_radius=2
    ),
    12: mp_drawing.DrawingSpec(
        color=(0, 255, 255),
        thickness=5,
        circle_radius=2
    ),

    # Anular: morado
    13: mp_drawing.DrawingSpec(
        color=(128, 0, 128),
        thickness=5,
        circle_radius=2
    ),
    14: mp_drawing.DrawingSpec(
        color=(128, 0, 128),
        thickness=5,
        circle_radius=2
    ),
    15: mp_drawing.DrawingSpec(
        color=(128, 0, 128),
        thickness=5,
        circle_radius=2
    ),
    16: mp_drawing.DrawingSpec(
        color=(128, 0, 128),
        thickness=5,
        circle_radius=2
    ),

    # Meñique: cian
    17: mp_drawing.DrawingSpec(
        color=(255, 255, 0),
        thickness=5,
        circle_radius=2
    ),
    18: mp_drawing.DrawingSpec(
        color=(255, 255, 0),
        thickness=5,
        circle_radius=2
    ),
    19: mp_drawing.DrawingSpec(
        color=(255, 255, 0),
        thickness=5,
        circle_radius=2
    ),
    20: mp_drawing.DrawingSpec(
        color=(255, 255, 0),
        thickness=5,
        circle_radius=2
    )
}

estilo_coneccion = mp_drawing.DrawingSpec(
    color=(0, 0, 0 ),
    thickness=2,
)

hands = mp_hands.Hands(
    static_image_mode= False,
    max_num_hands=1,
    model_complexity=0, 
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
)
		
# abrir camara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    hands.close()

    raise RuntimeError(
        "No se pudo abrir la cámara."
    )

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(
        frame,
        1
    )

    rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    resultado = hands.process(
        rgb
    )
    
    if resultado.multi_hand_landmarks:

        hand = (resultado.multi_hand_landmarks[0])

        mp_drawing.draw_landmarks(
            image= frame, 
            landmark_list =hand,#[], #hands
            connections=mp_hands.HAND_CONNECTIONS,#[],#mp_hands.HAND_CONNECTIONS
            landmark_drawing_spec =estilo_puntos ,
            connection_drawing_spec= estilo_coneccion
        )

        #ver los 63 datos
		
        datos =[]
        for lm in hand.landmark:
            datos.extend([
                lm.x,
                lm.y,
                lm.z
            ])
            #crear filas con igualdad de columnas
        datos_df = pd.DataFrame(
            [datos],
            columns=columnas
        )

        #predicicon del modelo 
        letra = modelo.predict(
            datos_df
        )[0]

        letra = str(
            letra
        ).strip().upper()

        #validacion de la b
        if letra == "B":

            if es_b_valida(hand):
                resultado_final = "B"

            else:
               resultado_final = "no reconocida"

        #validamos o
       # elif letra == "O":

        #    if es_o_valida(hand):
         #       resultado_final = "O"

          #  else:
           #     resultado_final = "no reconocida"

        #las clases que quedan
        else:
            resultado_final = letra
    
        #mostrar el resultado

        cv2.putText(
            frame,
            resultado_final,
            (50,150),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0, 0, 255),
            5
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

print("reconocimiento terminado (●'◡'●)")