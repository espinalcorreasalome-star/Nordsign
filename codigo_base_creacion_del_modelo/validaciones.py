import math
#validaciones geometricas para lasic

#Umbrales 

#letra b:
UMBRAL_DEDOS_JUNTOS_B = 0.80
UMBRAL_PULGAR_DENTRO_B= 0.95
UMBRAL_DEDO_RECTO_B= 170

#letra o
UMBRAL_O= 0.45

#funcion matematica base
def distancia_landmarks(hand_landmarks,i,j):
    p1 = hand_landmarks.landmarks[i]
    p2 = hand_landmarks.landmarks[j]

    return math.sqrt(
        (p1.x - p2.x)**2
        +(p1.y - p2.y)**2
        +(p1.z - p2.z)**2
    )

def angulo_entre_puntos(
          hand_landmarks,
          punto_a,
          punto_b,
          punto_c
):
    a= hand_landmarks.landmarks[punto_a]
    b= hand_landmarks.landmarks[punto_b]
    c = hand_landmarks.landmarks[punto_c]

    #vector que va desde b hacia a 
    vector_ba= (
        a.x - b.x,
        a.y - b.y,
        a.z - b.z
    )

    #vector que va desde b hacia c
    vector_bc = (
        c.x - b.x,
        c.y - b.y,
        c.z - b.z
    ) 

    producto_punto = (
        vector_ba[0] * vector_bc[0]
        + vector_ba[1] * vector_bc[1]
        +vector_ba[2] * vector_bc[2]
    )

    magnitud_ba = math.sqrt(
        vector_ba[0] **2
        + vector_ba[1] **2
        + vector_ba[2] **2
    )

    magnitud_bc = math.sqrt(
        vector_bc[0] **2
        + vector_bc[1] **2
        + vector_bc[2] **2
    )

    if magnitud_ba == 0 or magnitud_bc ==0: # pa que no divida entre 0
        return 0.0
    
    coseno = producto_punto/(
        magnitud_ba * magnitud_bc
    )

    coseno = max(  # evitar numeritos como 1.000000000000001 por ejemplo
        -1.0,
        min(1.0, coseno)
    )

    angulo_radianes = math.acos(coseno)

    return math.degrees(
        angulo_radianes
    )

def obtener_ancho_palma(hand_landmarks):
    return distancia_landmarks(
        hand_landmarks,
        5,
        17
    )

def obtener_angulos_dedos(hand_landmarks):
    return{

        "indice": min(
            angulo_entre_puntos(
                hand_landmarks,
                5,6,7
            ),
            angulo_entre_puntos(
                hand_landmarks,6,7,8
            )
        ),

        "medio": min(
            angulo_entre_puntos(
                hand_landmarks,
                9,10,11
            ),
            angulo_entre_puntos(
                hand_landmarks,
                10,11,12
            )
        ),

        "anular":min(
            angulo_entre_puntos(
                hand_landmarks,
                13,14,15
            ),
            angulo_entre_puntos(
                hand_landmarks,
                14,15,16
            )
        ),
        "meñique":min(
            angulo_entre_puntos(
                hand_landmarks,
                17,18,19
            ),
            angulo_entre_puntos(
                hand_landmarks,
                18,19,20
            )
        )
    }

def diagnostico_b(hans_landmarks):
    landmarks= hans_landmarks.landmark
    ancho_palma= obtener_ancho_palma(
        hans_landmarks
    )

    if ancho_palma <= 0:
        return{
            "dedos_rectos":False,
            "dedos_juntos" :False,
            "pulgar_dentro":False,
            "b_valida":False,
            "angulos":{},
            "distancias":{}
        }
   
    # 1 primera regla dedos rectos 
    angulos= obtener_angulos_dedos( 
        hans_landmarks
    )

    dedos_rectos_por_angulo = all(
        valor >= UMBRAL_DEDO_RECTO_B
        for valor in angulos.values()
    )
    
    dedos_hacia_arriba = (
        landmarks[8].y < landmarks[6].y
        and landmarks[12].y < landmarks[10].y
        and landmarks[16].y < landmarks[14].y
        and landmarks[20].y < landmarks[18].y
    )

    dedos_rectos=(
        dedos_rectos_por_angulo
        and dedos_hacia_arriba
    )
    # 2 segund regla  dedos juntos 
    distancia_8_12=(
        distancia_landmarks(
            hans_landmarks,
            8,
            12
        )/ ancho_palma
    )
    
    distancia_12_16=(
        distancia_landmarks(
            hans_landmarks,
            12,
            16
        )/ ancho_palma
    )

    distancia_16_20 =(
        distancia_landmarks(
            hans_landmarks,
            16, 
            20
        )/ ancho_palma
    )

    dedos_juntos=(
        distancia_8_12 <= UMBRAL_DEDOS_JUNTOS_B
        and distancia_12_16 <= UMBRAL_DEDOS_JUNTOS_B
        and distancia_16_20 <= UMBRAL_DEDOS_JUNTOS_B
    )

    #3 tercera regla pulgar andentro de l aplma 
    distancia_4_13 = (
         distancia_landmarks( 
             hans_landmarks,
             4,
             13 
        ) / ancho_palma 
    )

    distancia_4_17 = (
         distancia_landmarks( 
             hans_landmarks,
             4,
             17 
        ) / ancho_palma
     )
    
    pulgar_dentro = (
         distancia_4_13
         <= UMBRAL_PULGAR_DENTRO_B
        
        or distancia_4_17
        <= UMBRAL_PULGAR_DENTRO_B 
    )

    b_valida = (
         dedos_rectos
        and dedos_juntos
        and pulgar_dentro 
    )

    return {
         "dedos_rectos": dedos_rectos,
         "dedos_juntos": dedos_juntos,
         "pulgar_dentro": pulgar_dentro,
         "b_valida": b_valida,

         "angulos": angulos,

         "distancias": { 
             "8-12": distancia_8_12,
             "12-16": distancia_12_16, 
             "16-20": distancia_16_20, 
             "4-13": distancia_4_13, 
             "4-17": distancia_4_17 
            } 
   }

def es_b_valida (hand_landmarks):
    return diagnostico_b(
        hand_landmarks
    )["es_b_valida"]

# letra 0

def diagnostico_o(hand_landmarks):
    ancho_palma = obtener_ancho_palma(
         hand_landmarks 
    ) 

    if ancho_palma <= 0:
        return {
            "puntas_cerca": False, 
            "o_valida": False, 
            "distancias": {} 
        }
    
    distancia_4_8 =( 
        distancia_landmarks(
             hand_landmarks,
             4, 
             8 
        ) / ancho_palma 
    ) 
    
    distancia_4_12 = (
         distancia_landmarks(
              hand_landmarks, 
              4, 
              12 
            ) / ancho_palma 
    )

    distancia_4_16 = (
         distancia_landmarks(
           hand_landmarks, 
           4, 
           16 
        ) / ancho_palma
    ) 

    distancia_4_20 = (
         distancia_landmarks(
            hand_landmarks,
            4,
            20 
         ) / ancho_palma
    )
    puntas_cerca = (
        distancia_4_8 <= UMBRAL_O 
        and distancia_4_12 <= UMBRAL_O 
        and distancia_4_16 <= UMBRAL_O 
        and distancia_4_20 <= UMBRAL_O
    ) 
    return { 
        "puntas_cerca": puntas_cerca, 
        "o_valida": puntas_cerca,

        "distancias": { 
            "4-8": distancia_4_8, 
            "4-12": distancia_4_12, 
            "4-16": distancia_4_16, 
            "4-20": distancia_4_20 
        } 
    }

def es_o_valida(hand_landmarks):
    return diagnostico_o(
        hand_landmarks
    )["o_valida"]
