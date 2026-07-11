import cv2
import mediapipe as mp
import os
import csv


#configuracion

LETRAS = ["A", "E", "I", "O", "U"]

MUESTRAS_POR_LETRA = 50 #la primera vez toma 50 ,luego se van sumadon :)
ARCHIVO = "vocales.csv"

# configuraciones mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,# es el numero de manos que detecta 
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
)


#abrimos camara
cap = cv2.VideoCapture(0)#captura la camara ,si es 0 es la camara principal del dispositivo y si es 1 son las camaparas externas que se conectaron al dispocitivo :)

if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    hands.close()
    raise SystemExit




if not os.path.exists(ARCHIVO):
    with open(
        ARCHIVO,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as archivo_csv:

        writer = csv.writer(archivo_csv)

        header = []

        for i in range(21):
            header += [f"x{i}", f"y{i}", f"z{i}"]

        header.append("letra")
        writer.writerow(header)




contador = 0
letra_actual = None


print("Presiona la vocal que quieras capturar: A, E, I, O o U ")
print("Presiona ESC para salir ")


# inicio del bucle para capturar las vocales

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # Detectar la mano
    resultado = hands.process(frame_rgb)

    if resultado.multi_hand_landmarks:
        hand = resultado.multi_hand_landmarks[0]

        # Dibujar puntos y conexiones
        mp_drawing.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

        # Guardar muestras
        if (
            letra_actual is not None
            and contador < MUESTRAS_POR_LETRA
        ):
            fila = []

            for lm in hand.landmark:
                fila.extend([
                    lm.x,
                    lm.y,
                    lm.z
                ])

            # Agregar la letra una sola vez
            fila.append(letra_actual)

            with open(
                ARCHIVO,
                mode="a",
                newline="",
                encoding="utf-8"
            ) as archivo_csv:

                writer = csv.writer(archivo_csv)
                writer.writerow(fila)

            contador += 1

            print(
                f"{letra_actual}: "
                f"{contador}/{MUESTRAS_POR_LETRA}",
                end="\r"
            )

        # Finalizar captura actual
        if (
            letra_actual is not None
            and contador >= MUESTRAS_POR_LETRA
        ):
            print(
                f"\nLetra {letra_actual} "
                f"capturada correctamente (●'◡'●) "
            )

            letra_actual = None
            contador = 0

    # texto de la pantalla

    if letra_actual is None:
        texto_estado = "Presiona A, E, I, O o U"

    else:
        texto_estado = (
            f"Capturando {letra_actual}: "
            f"{contador}/{MUESTRAS_POR_LETRA}"
        )

    cv2.putText(
        frame,
        texto_estado,
        (15, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        "ESC para salir",
        (15, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.imshow(
        "Captura de vocales",
        frame
    )

    # para el teclado 

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break

    if key != 255:
        tecla = chr(key).upper()

        if tecla in LETRAS:
            letra_actual = tecla
            contador = 0

            print(
                f"\nCapturando letra "
                f"{letra_actual}..."
            )


cap.release()
cv2.destroyAllWindows()
hands.close()

print("\nPrograma terminado.")