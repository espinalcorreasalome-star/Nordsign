import cv2
import mediapipe as mp
import os 
import csv 

#configuracion 
letras = ["A", "e", "i","o","u"]
muestra_por_letra = 50 #la primera vez toma 50 ,luego se van sumadon :)
archivo = "vocales.csv"

# configuraciones mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode = False,
    max_num_hands = 1, # este es el numero de manos maximo que detecta 
    min_detection_confidence = 0.7 # esta es la confianza minima para detectar una mano
)
cap = cv2.VideoCapture(0)#captura la camara ,si es 0 es la camara principal del dispositivo y si es 1 son las camaparas externas que se conectaron al dispocitivo :)

# esto es para crear el cvs por si no existe :o

if not os.path.exists(archivo):
    with open(archivo, mode='w', newline='') as f:
        writer = csv.writer(f)
        header = []
        for i in range(21):
           header += [f"x{i}", f"y{i}",f"z{i}"]
        header += ["letra"]
        writer.writerow(header)

    print("presiona la vocal que quieras capturar (A,E,I,O,U)")
    print("presiona ESC para salir")

    contador = 0
    letra_actual = None

    while True:
       ret, frame = cap.read()
       if not ret:
          break 
       
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = hands.process(frame_rgb)

    if resultado.multi_hand_landmarks:
       hand = resultado.multi_hand_landmarcks[0]
       mp.solutions.drawing_utils.draw_landmarks(
          frame, hand, mp_hands.HAND_CONNECTIONS
       )

       if letra_actual is not None and contador < muestra_por_letra:
            fila = []
            for lm in hand.landmark:
               fila.extend([lm.x, lm.y, lm.z])
               fila.append(letra_actual)

               with open(archivo, "a", newline="") as f:
                  writer = csv.writer(f)
                  writer.writerow(fila)
            contador += 1
            print(f"{letra_actual}:{contador}/{muestra_por_letra}")
       if contador == muestra_por_letra:
          letra_actual = None
          contador =0
          print("letra capturada (●'◡'●)") 
    cv2.imshow("captura de vocales", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
    elif chr(key).upper() in LETRAS:
        letra_actual = chr(key).upper()
        contador = 0
        print(f"Capturando letra {letra_actual}")
	
cap.release()
cv2.destroyAllWindows()
