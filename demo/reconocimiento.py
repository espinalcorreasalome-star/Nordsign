import os
import sys

import cv2
import joblib
import mediapipe as mp
import pandas as pd

DEMO_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

BASE_DIR = os.path.dirname(
    DEMO_DIR
)

ARCHIVO_MODELO = os.path.join(
    BASE_DIR,
    "modelo_lsc.pkl"
)

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from codigo_base_creacion_del_modelo.validaciones import (
    es_b_valida
) 

#clases de reconocimiento hace todo menos la camara 
class ReconocedorLSC:
    def __init__(self):
        self.modelo = None
        self.columnas = None
        self.clases = None

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self._cargar_modelo()
        self._configurar_estilos()
        self._configurar_mediapipe()
    #cargar modelo
    def _cargar_modelo(self):
     if not os.path.exists(ARCHIVO_MODELO):
        raise FileNotFoundError(
            "no se encontro el modelo "
            f"ruta buscada:\n{ARCHIVO_MODELO}"
        )
    
     paquete = joblib.load(
        ARCHIVO_MODELO
     )

     if not isinstance(paquete, dict):
        raise TypeError(
            "el modelo_lsc no contiene"
            "el paquete esperado"
        )
    
     claves_necesarias = {
        "modelo",
        "columnas",
        "clases"
     }

     claves_faltantes = (
            claves_necesarias
            - set(paquete.keys())
        )

     if claves_faltantes:
            raise KeyError(
                "Al paquete del modelo le faltan estas claves: "
                f"{claves_faltantes}"
            )

     self.modelo = paquete["modelo"]
     self.columnas = paquete["columnas"]
     self.clases = paquete["clases"]

     if len(self.columnas) != 63:
            raise ValueError(
                "El modelo debe esperar 63 características.\n"
                f"Características encontradas: {len(self.columnas)}"
            )

     print("Modelo LASIC cargado correctamente.")
     print(f"Clases disponibles: {self.clases}")
     print(f"Características esperadas: {len(self.columnas)}")
    #estilos de mediapipe
    def _configurar_estilos(self):
     self.estilo_puntos ={
        #muñeca blanca 
         0: self.mp_drawing.DrawingSpec(
              color = (255, 255, 255),
              thickness = 2,
              circle_radius = 3
        ),

        #pulgar rojo
        1: self.mp_drawing.DrawingSpec(
              color = (0, 0, 255),
              thickness = 4,
              circle_radius = 3
        ),

        2: self.mp_drawing.DrawingSpec(
              color = (0, 0, 255),
              thickness = 4,
              circle_radius = 3
        ),

        3: self.mp_drawing.DrawingSpec(
              color = (0, 0, 255),
              thickness = 4,
              circle_radius = 3
        ),

        4: self.mp_drawing.DrawingSpec(
              color = (0, 0, 255),
              thickness = 4,
              circle_radius = 3
        ),

        #indice verde
        5: self.mp_drawing.DrawingSpec(
              color = (0, 255, 0),
              thickness = 4,
              circle_radius = 3
        ),

        6: self.mp_drawing.DrawingSpec(
              color = (0, 255, 0),
              thickness = 4,
              circle_radius = 3
        ),

        7: self.mp_drawing.DrawingSpec(
              color = (0, 255, 0),
              thickness = 4,
              circle_radius = 3
        ),

        8: self.mp_drawing.DrawingSpec(
              color = (0, 255, 0),
              thickness = 4,
              circle_radius = 3
        ),

        #medio amarrilo
        9: self.mp_drawing.DrawingSpec(
              color = (0, 255, 255),
              thickness = 4,
              circle_radius = 3
        ),

        10: self.mp_drawing.DrawingSpec(
              color = (0, 255, 255),
              thickness = 4,
              circle_radius = 3
        ),

        11: self.mp_drawing.DrawingSpec(
              color = (0, 255, 255),
              thickness = 4,
              circle_radius = 3
        ),

        12: self.mp_drawing.DrawingSpec(
              color = (0, 255, 255),
              thickness = 4,
              circle_radius = 3
        ),

        #anular morado 
        13: self.mp_drawing.DrawingSpec(
              color = (128, 0, 128),
              thickness = 4,
              circle_radius = 3
        ),

        14: self.mp_drawing.DrawingSpec(
              color = (128, 0, 128),
              thickness = 4,
              circle_radius = 3
        ),

        15: self.mp_drawing.DrawingSpec(
              color = (128, 0, 128),
              thickness = 4,
              circle_radius = 3
        ),

        16: self.mp_drawing.DrawingSpec(
              color = (128, 0, 128),
              thickness = 4,
              circle_radius = 3
        ),

        #meñique azul
        17: self.mp_drawing.DrawingSpec(
              color = (255, 255, 0),
              thickness = 4,
              circle_radius = 3
        ),

        18: self.mp_drawing.DrawingSpec(
              color = (255, 255, 0),
              thickness = 4,
              circle_radius = 3
        ),

        19: self.mp_drawing.DrawingSpec(
              color = (255, 255, 0),
              thickness = 4,
              circle_radius = 3
        ),

        20: self.mp_drawing.DrawingSpec(
              color = (255, 255, 0),
              thickness = 4,
              circle_radius = 3
        ),
     }

     self.estilo_conexiones = (
         self.mp_drawing.DrawingSpec(
              color = (0, 0, 0),
              thickness = 2
         )
        )
    #configuracion mediapipe
    def _configurar_mediapipe(self):
      self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=0.70,
            min_tracking_confidence=0.60
        )
    @staticmethod
    def extraer_landmarks(hand_landmarks):
        datos = []

        for landmark in hand_landmarks.landmark:
            datos.extend([
                landmark.x,
                landmark.y,
                landmark.z
            ])

        return datos
    # predecir letra 
    def predecir_letra(self,hand_landmarks):
     datos = self.extraer_lamdmarks(
          hand_landmarks
        )

     if len(datos) != len(self.columnas):
      raise ValueError(
      "La cantidad de landmarks no coincide con "
      "las características del modelo.\n"
      f"Datos detectados: {len(datos)}\n"
      f"Datos esperados: {len(self.columnas)}"    
     )
     
     datos_df = pd.DataFrame(
      [datos],
      columns=self.columnas
     )

     letra = self.modelo.prefict(
      datos_df
     )[0]

     return str(
      letra
     ).strip().upper()
    #aplicamos validaciones 
    @staticmethod
    def validar_resultado(
        letra,
        hand_landmarks
    ):
      if letra == "B":
         if es_b_valida(hand_landmarks):
            return "B"
          
         return "no reconocida"
      
      return letra
    #procesamos los fotogramas 
    def procesar_frames(self, frame):
     if frame is None:
         return None, "",False
    
     frame = cv2.flip(
         frame,
         1
        )

     frame_rgb = cv2.cvtColor(
         frame,
         cv2.COLOR_BGR2RGB
        )

     frame_rgb.flags.writeable = False

     resultado_mediapipe = self.hands.process(
        frame_rgb
     )

     frame_rgb.flags.writeable = True

     if not resultado_mediapipe.multi_hand_landmarks:
          return frame, "", False

     hand_landmarks = (
         resultado_mediapipe
         .multi_hand_landmarks[0]
        )
     self.mp_drawing.draw_landmarks(
        image=frame,
        landmark_list=hand_landmarks,
        connections=self.mp_hands.HAND_CONNECTIONS,
        landmark_drawing_spec=self.estilo_puntos,
        connection_drawing_spec=self.estilo_conexiones
     )

     letra_modelo = self.predecir_letra(
            hand_landmarks
        )

     resultado_final = self.validar_resultado(
         letra_modelo,
         hand_landmarks
        )

     return(
     frame,
     resultado_final,
     True
     )
    #cerrar mediapipe
    def cerrar(self):
     if self.hands is not None:
          self.hands.close()
          self.hands = None

if __name__ == "__main__":
    reconocedor = ReconocedorLSC()

    print("\nPrueba completada.")
    print(
        "El modelo y MediaPipe se cargaron correctamente."
    )

    reconocedor.cerrar()