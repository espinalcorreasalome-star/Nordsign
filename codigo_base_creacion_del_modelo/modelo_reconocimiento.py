import os
from collections import Counter, deque

import cv2
import mediapipe as mp
import joblib
import pandas as pd

from validaciones import(
    es_b_valida,
)

#configuracion
BASE_DIR = os.path.dirname(
    os.path.dirname(
    os.path.abspath(__file__))
)

ARCHIVO_MODELO = os.path.join(
     BASE_DIR,
     "modelo_lsc.pkl"
)

PROCESAR_CADA_N_FRAMES= 3
TAMANO_HISTORIAL =5

# Cargar el modelo

print("Carpeta principal:")
print(BASE_DIR)

print("\nBuscando modelo en:")
print(ARCHIVO_MODELO)

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

claves_necesarias = {
    "modelo",
    "columnas",
    "clases"
}

claves_faltantes=(
    claves_necesarias
    - set(paquete.keys())
)

if claves_faltantes:
    raise KeyError(
        "al paquete del modelo le faltan estas claves:"
        f"{claves_faltantes}"
    )

#sacamos los elementos del diccionario 
modelo = paquete["modelo"]
columnas = paquete["columnas"]
clases =paquete["clases"]

print("modelo cargado adecuadamente")
print("\n clases aprendidas: {clases}")
print(f"Características esperadas: {len(columnas)}")
	
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
    min_detection_confidence=0.70,
    min_tracking_confidence=0.60
)
		
# abrir camara
cap = cv2.VideoCapture(0)

cap.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    640
)

cap.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    480
)


if not cap.isOpened():
    hands.close()

    raise RuntimeError(
        "No se pudo abrir la cámara."
    )

#funciones del reconocimiento (●'◡'●)
def extraer_landmarks(hand_landmarks):
    datos = []

    for landmark in hand_landmarks.landmark:
        datos.extend([
            landmark.x,
            landmark.y,
            landmark.z
        ])

    return datos
    
def  predecir_clase(hand_landmarks):
    datos = extraer_landmarks(
        hand_landmarks
    )

    if len(datos) != len(columnas):
        raise ValueError(
            "la cantidad de datos detectados no coincide"
            "con las columnas del entrenamient.\n"
            f"datos detectados:{len(datos)}\n"
            f"columnas esperadas:{len(columnas)}"
        )
    
    datos_df = pd.DataFrame(
        [datos],
        columns=columnas
    )

    clase_predicha = modelo.predict(
        datos_df
    )[0]

    return str(
        clase_predicha
    ).strip().upper()

#filtrado de b
def aplicar_regla_b(  
        clase_predicha,
        hand_landmarks
    ):
    if clase_predicha == "B":

        if es_b_valida(hand_landmarks):
            return "B"

        return "B INCORRECTA"
    
    return clase_predicha

#estabilizar prediccion
def obtener_resultado_estable(historial):
    if not historial:
        return "esperando"

    conteo = Counter(
        historial
    )

    resultado_mas_repetido = (
        conteo.most_common(1)[0][0]
    )

    return resultado_mas_repetido

#variables del programa 
contador_frames = 0
resultado_final = "ESPERANDO"
historial_resultados = deque(
    maxlen=TAMANO_HISTORIAL
)


print("\nReconocimiento iniciado.")
print("Presiona ESC para salir.\n")

#reconocimiento

while True:
    ret, frame = cap.read()
    if not ret:
        print(
            "No se pudo capturar la imagen."
        )
        break

    frame = cv2.flip(
        frame,
        1
    )

    frame_rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    frame_rgb.flags.writeable = False

    resultado_mediapipe = hands.process(
        frame_rgb
    )

    frame_rgb.flags.writeable = True

    contador_frames += 1

    mano_visible = bool(
        resultado_mediapipe.multi_hand_landmarks
    )
    
    if mano_visible:

        hand = ( 
            resultado_mediapipe
            .multi_hand_landmarks[0]
        )

        mp_drawing.draw_landmarks(
            image= frame, 
            landmark_list =hand,#[], #hands
            connections=mp_hands.HAND_CONNECTIONS,#[],#mp_hands.HAND_CONNECTIONS
            landmark_drawing_spec =estilo_puntos ,
            connection_drawing_spec= estilo_coneccion
        )
		
        #ejecutar ramdom forest cada n frames
        if (
            contador_frames
            % PROCESAR_CADA_N_FRAMES
            == 0
        ):

            clase_modelo = predecir_clase(
                hand
            )

            resultado_validado = aplicar_regla_b(
                clase_modelo,
                hand
            )

            historial_resultados.append(
                resultado_validado
            )

            resultado_final = (
                obtener_resultado_estable(
                    historial_resultados
                )
            )
        else:
            historial_resultados.clear()
            resultado_final = "SIN MANO"

        if resultado_final in {
              "SIN MANO",
             "B INCORRECTA"
         }:

         # Rojo para advertencia
          color_texto = (0, 0,255)

        else:
           # Verde para clases reconocidas
           color_texto = ( 0, 220,0 )

        cv2.putText(
            frame,
            resultado_final,
            (20,80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            color_texto,
            4
        )  

    cv2.imshow(
     "LASIC - Reconocimiento LSC",
     frame
   )

    tecla = cv2.waitKey(1) & 0xFF

    if tecla== 27:
        break
  
# cerrar todo 
cap.release()
cv2.destroyAllWindows()
hands.close()

print("reconocimiento terminado (●'◡'●)")