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
def distancia_landmarks(hand_landmarks, i, j):
    p1 = hand_landmarks.landmark[i]
    p2 = hand_landmarks.landmark[j]

    return math.sqrt(
        (p1.x - p2.x) ** 2
        + (p1.y - p2.y) ** 2
        + (p1.z - p2.z) ** 2
    )

def angulo_entre_puntos(
          hand_landmarks,
          punto_a,
          punto_b,
          punto_c
):
    a= hand_landmarks.landmark[punto_a]
    b= hand_landmarks.landmark[punto_b]
    c = hand_landmarks.landmark[punto_c]

    #vector que va desde b hacia a 
    vector_ba= (
        a.x - b.x,
        a.y - b.y,
    )

    #vector que va desde b hacia c
    vector_bc = (
        c.x - b.x,
        c.y - b.y,
    ) 

    producto_punto = (
        vector_ba[0] * vector_bc[0]
        + vector_ba[1] * vector_bc[1]
    )

    magnitud_ba = math.sqrt(
        vector_ba[0] **2
        + vector_ba[1] **2
    )

    magnitud_bc = math.sqrt(
        vector_bc[0] **2
        + vector_bc[1] **2
    )

    if magnitud_ba == 0 or magnitud_bc ==0: # pa que no divida entre 0
        return 0
    
    coseno = producto_punto/(
        magnitud_ba * magnitud_bc
    )

    coseno = max(  # evitar numeritos como 1.000000000000001 por ejemplo
        -1.0,
        min(1.0, coseno)
    )


    return math.degrees(
        math.acos(coseno)
    )

def dedos_rectos_b(hand_landmarks):
    umbral_articulacion_inferior = 155
    umbral_articulacion_superior = 150

    dedos={
        "indice":(5,6,7,8),
        "medio":(9,10,11,12),
        "anular":(13,14,15,16),
        "meñique":(17,18,19,20)
    }
    resultados=[]

    for nombre, puntos in dedos.items():
        base, articulacion_1, articulacion_2, punta = puntos

        angulo_inferior = angulo_entre_puntos(
            hand_landmarks,
            base,
            articulacion_1,
            articulacion_2
        )

        angulo_superior = angulo_entre_puntos(
            hand_landmarks,
            articulacion_1,
            articulacion_2,
            punta
        )

        if nombre == "menique":
            umbral_inferior = 145
            umbral_superior = 140
        else:
            umbral_inferior = 155
            umbral_superior = 150

        dedo_recto =(
            angulo_inferior >= umbral_inferior
            and angulo_superior >= umbral_superior
        )

        resultados.append(
            dedo_recto
        )

        print(
            f"{nombre}: "
            f"{angulo_inferior:.1f} /"
            f"{angulo_superior:.1f}="
            f"{dedo_recto}"
        )
        return all(resultados)

def dedos_juntos_b(hand_landmarks):
    ancho_palma =distancia_landmarks(
        hand_landmarks,
        5,
        17
    )

    if ancho_palma<=0:
        return False
    
    distancia_8_12 = distancia_landmarks(
        hand_landmarks,
        8,
        12
    )

    distancia_12_16= distancia_landmarks(
        hand_landmarks,
        12,
        16
    )


    distancia_7_11 = distancia_landmarks(
        hand_landmarks,
        7,
        11
    )

    distancia_11_15= distancia_landmarks(
        hand_landmarks,
        11,
        15
    )


    limite_articulaciones = ancho_palma*0.43
    limite_puntas = ancho_palma *0.65

    articulaciones_juntas= (
        distancia_7_11 <= limite_articulaciones
        and distancia_11_15 <= limite_articulaciones
    )

    puntas_juntas =(
        distancia_8_12 <= limite_puntas
        and distancia_12_16 <= limite_puntas
    )

    return(
        articulaciones_juntas
        and puntas_juntas
    )

def pulgar_dentro_b(hand_landmarks):

    ancho_palma =distancia_landmarks(
        hand_landmarks,
        5,
        17
    )

    if ancho_palma == 0:
        return False
    
    distancia_4_5 = distancia_landmarks(
        hand_landmarks,
        4,
        5
    )

    distancia_4_13 = distancia_landmarks(
        hand_landmarks,
        4,
        13
    )

    distancia_4_17 = distancia_landmarks(
        hand_landmarks,
        4,
        17
    )

    limite = ancho_palma * 0.90

    return(
        distancia_4_5 <= limite
        or distancia_4_13 <= limite
        or distancia_4_17 <= limite
    )

def diagnostico_b(hans_landmarks):
    regla_rectos = dedos_rectos_b(
        hans_landmarks
    )

    regla_juntos = dedos_juntos_b(
        hans_landmarks
    )

    regla_pulgar = pulgar_dentro_b(
        hans_landmarks
    )

    b_valida =(
        regla_rectos
        and regla_juntos
        and regla_pulgar
    )

    return {
        "valida": b_valida,
        "dedos_rectos": regla_rectos,
        "dedos_juntos": regla_juntos,
        "pulgar_dentro": regla_pulgar
    }

def es_b_valida(hand_landmarks):
    resultado = diagnostico_b(hand_landmarks)

    print(
        "B"
        f"rectos:{resultado['dedos_rectos']} "
        f"juntos:{resultado['dedos_juntos']} "
        f"pulgar:{resultado['pulgar_dentro']} ",
        end="\r"
    )
    return resultado["valida"]
    
# letra 0

def diagnostico_o(hand_landmarks):
    ancho_palma =distancia_landmarks(
        hand_landmarks,
        5,
        17
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
