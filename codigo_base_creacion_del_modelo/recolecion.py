import cv2
import mediapipe as mp
import os
import csv
import threading

#configuracion

MUESTRAS_POR_PALABRA = 50 #la primera vez toma 50 ,luego se van sumadon :)
ARCHIVO = "vocales.csv"

# definimos funciones 

def leer_clases_existentes(path_csv: str): 
    """
    da como respuesta 
    la lista de las clases ordenada
    conteo por clase creada
    """
    if not os.path.exists(path_csv):
        return [], {}
    conteo = {}

    with open( path_csv, "r", newline="",encoding="utf-8") as f:

        reader = csv.reader(f)
        header = next(reader, None)

        for row in reader:
            if not row:
                continue
            palabra = row[-1].strip()

            if palabra == "":
                continue 

            conteo[palabra] = conteo.get(palabra, 0) + 1 

    clases = sorted(conteo.keys(), key=lambda x: x.lower())
    return clases, conteo
 
#  funcion que me da la info de las clases y cuantas hay

def imprimir_clases(clases, conteo):
    if not clases:
        print("no hay clases creadas un (●'◡'●)")
        return
    print("clases ya creadas ")

    for i, clase in enumerate(clases, 1):
        print(f"{i}.{clase}" f" {conteo[clase]} muestras")
    print("") 

# creamos csv por si no existe :O

if not os.path.exists(ARCHIVO):
    with open(
        ARCHIVO,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)
        header = []

        for i in range(21):
            header += [
                f"x{i}",
                f"y{i}",
                f"z{i}"
            ]

        header.append("palabra")
        writer.writerow(header)
        
# mostrar clases existentes 

clases_existentes, conteo_existente = (leer_clases_existentes(ARCHIVO))

imprimir_clases(clases_existentes, conteo_existente)

# configuraciones mediapipe

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# estilo de puntos de la mano

estilo_puntos = mp_drawing.DrawingSpec(
    color = (0, 255, 255),
    thickness =2,
    circle_radius=5
)

#estilo de las lineas entre los puntos 
estilo_conexiones = mp_drawing.DrawingSpec(
    color=(255, 0, 255),
    thickness=3,
    circle_radius=2
)

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1, # es el numero de manos que detecta 
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6
)

#abrimos camara

cap = cv2.VideoCapture(0) #captura la camara ,si es 0 es la camara principal del dispositivo y si es 1 son las camaparas externas que se conectaron al dispocitivo :)

if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    hands.close()
    raise SystemExit


#variables compartidas
lock = threading.Lock()

palabra_actual = None
contador = 0
salir = False

# hilo de la consola 

def hilo_consola():
    """
    con esto es posible escribir palabras y comandos
    sin detener la camara (●'◡'●)
    """
    global palabra_actual, contador, salir 

    print("Esctibe una palabra y presiona entrer")
    print("comandos: listar / salir\n")

    while True:
    
       try:
            texto = input ("palabra>").strip()

       except EOFError:
           texto = "salir" 

       if texto == "":
            continue 
    
       if texto.lower() == "salir":
         
          with lock:
              salir = True

          break
       if texto.lower() == "listar":
         clases, conteo = leer_clases_existentes(ARCHIVO)

         imprimir_clases(clases, conteo)
         continue 
    
       with lock:
        palabra_actual = texto
        contador = 0

       print(f"capturando '{texto}'" f"0/{MUESTRAS_POR_PALABRA}")

        
# iniciamos el hilo

t= threading.Thread( target=hilo_consola, daemon=True )

t.start()

# loop principal
while True:
    with lock:
        if salir:
            break

        palabra = palabra_actual
        c = contador
    
    ret, frame =cap.read()

    if not ret:
        break

    frame = cv2.flip (frame, 1)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    resultado = hands.process(frame_rgb)

    if resultado.multi_hand_landmarks:
        hand = resultado.multi_hand_landmarks [0]

        mp_drawing.draw_landmarks(
             frame,
             hand,
             mp_hands.HAND_CONNECTIONS,
             estilo_puntos,
             estilo_conexiones
             )

        if (palabra is not None 
            and c < MUESTRAS_POR_PALABRA):
            fila = []

            for lm in hand.landmark:
                fila.extend([lm.x,
                             lm.y,
                             lm.z
                             ])
            fila.append(palabra)

            with open( ARCHIVO, "a", newline ="", encoding="utf-8") as f:
               writer = csv.writer(f) 
               writer.writerow(fila)

            with lock:
                contador += 1
                c2 = contador 
            
            c = c2

            print(f"'{palabra}':" f"{c2}/{MUESTRAS_POR_PALABRA}")

            if c2 >= MUESTRAS_POR_PALABRA:
                with lock :
                    palabra_actual = None
                    contador = 0
                print(f"clase completada:" f"'{palabra}'")
           

    if palabra:

        estado =( f"capturando: {palabra}" f"({c}/{MUESTRAS_POR_PALABRA})")
    
    else:
        
        estado= ("esperando palabra en consola")

    cv2.putText( frame, estado, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("captura de datos", frame)

    if cv2.waitKey(1) & 0xFF == 27:

        with lock:
            salir = True

        break

#para cerrar todo 

cap.release()
cv2.destroyAllWindows()
hands.close()

print("recoleccion terminada,bye (●'◡'●) ")