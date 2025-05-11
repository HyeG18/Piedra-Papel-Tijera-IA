from random import choice 
import cv2
import numpy as np
import time

CLASS_MAP = {
    0: "Ninguno",
    1: "Piedra",
    2: "Papel",
    3: "Tijera",
    4: "Inicio"
}

def mapeado(val):
    return CLASS_MAP[val]

def determinar_ganador(jugador, cpu):
    msgJugador = "Ganaste"
    msgCpu = "Perdiste"

    if jugador == cpu:
        return "Empate"
    
    if jugador == "Piedra":
        if cpu == "Papel":
            return msgCpu
        else:
            return msgJugador

    if jugador == "Papel":
        if cpu == "Tijera":
            return msgCpu
        else:
            return msgJugador

    if jugador == "Tijera":
        if cpu == "Piedra":
            return msgCpu
        else:
            return msgJugador

# Simulación: No cargamos el modelo porque aún no está listo
# model = keras.models.load_model('modelo.h5')

cap = cv2.VideoCapture(0)

prev_jugada = None
nombre_jugada_jugador = "Ninguno"
nombre_jugada_cpu = "Ninguno"
nombre_ganador = "Esperando..."

start_time = time.time()

working = False

victorias = 0
derrotas = 0
empates = 0

ciclos = 0

movimientoID = 0

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    height, width, _ = frame.shape

    bar_height = height // 8

    cv2.rectangle(frame, (0, 0), (width, bar_height), (0, 0, 0), -1)

    cv2.rectangle(frame, (0, height - bar_height), (width, height), (0, 0, 0), -1)

    mensaje_salida = "Presiona 'Q' para salir"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1 
    thickness = 2 
    text_size = cv2.getTextSize(mensaje_salida, font, font_scale, thickness)[0]
    text_x = width - text_size[0] - 10 
    text_y = height - 10
    cv2.putText(frame, mensaje_salida, (text_x, text_y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

    rect_width = 250
    rect_height = 250 
    offset_x = int(width * 0.2)
    rect_player_x1 = (width - rect_width) // 2 - offset_x 
    rect_player_y1 = (height - rect_height) // 2
    rect_player_x2 = rect_player_x1 + rect_width
    rect_player_y2 = rect_player_y1 + rect_height
    rect_cpu_x1 = (width - rect_width) // 2 + offset_x
    rect_cpu_y1 = (height - rect_height) // 2
    rect_cpu_x2 = rect_cpu_x1 + rect_width
    rect_cpu_y2 = rect_cpu_y1 + rect_height
    
    cv2.rectangle(frame, (rect_player_x1, rect_player_y1), (rect_player_x2, rect_player_y2), (255, 255, 255), 2)

    if working:
        cv2.rectangle(frame, (rect_cpu_x1, rect_cpu_y1), (rect_cpu_x2, rect_cpu_y2), (255, 255, 255), 2)

    roi = frame[rect_player_y1:rect_player_y2, rect_player_x1:rect_player_x2]

    if working:
      elapsed_time = time.time() - start_time

      contador_font = cv2.FONT_HERSHEY_SIMPLEX
      contador_font_scale = 2  
      contador_thickness = 4  
      contador_text = ""

      if elapsed_time <= 1.5:
        contador_text = "3"
      elif elapsed_time <= 3:
        contador_text = "2"
      elif elapsed_time <= 4.5:
        contador_text = "1"

      if contador_text:
        text_size = cv2.getTextSize(contador_text, contador_font, contador_font_scale, contador_thickness)[0]
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2 
        cv2.putText(frame, contador_text, (text_x, text_y), contador_font, contador_font_scale, (0, 0, 0), contador_thickness, cv2.LINE_AA)

      if ciclos < 1 and elapsed_time <= 1.5:
        partida_font = cv2.FONT_HERSHEY_DUPLEX
        partida_font_scale = 1.5 
        partida_thickness = 2 
        partida_text = "Partida iniciada"
        partida_text_size = cv2.getTextSize(partida_text, partida_font, partida_font_scale, partida_thickness)[0]
        partida_text_x = (width - partida_text_size[0]) // 2 
        partida_text_y = text_y - 175
        cv2.putText(frame, partida_text, (partida_text_x, partida_text_y), partida_font, partida_font_scale, (0, 210, 0), partida_thickness, cv2.LINE_AA)

      if elapsed_time > 4.5:
        cv2.imwrite('gesture.jpg', roi)
        start_time = time.time()

        movimientoID = choice([1, 2, 3])
        nombre_jugada_jugador = mapeado(movimientoID)

        ciclos += 1
        if nombre_jugada_jugador != "Ninguno" and nombre_jugada_jugador != "Inicio":
            nombre_jugada_cpu = choice(["Piedra", "Papel", "Tijera"])
            nombre_ganador = determinar_ganador(nombre_jugada_jugador, nombre_jugada_cpu)
            if nombre_ganador == "Ganaste":
                victorias += 1
            elif nombre_ganador == "Perdiste":
                derrotas += 1
            else:
                empates += 1
        else:
            nombre_jugada_cpu = "Ninguno"
            nombre_ganador = "Esperando..."

      if nombre_jugada_cpu in ["Piedra", "Papel", "Tijera"]:
        ruta_imagen = f"imagenes/{nombre_jugada_cpu.lower()}.png"
        imagen_cpu = cv2.imread(ruta_imagen)
    
        if imagen_cpu is not None:
          imagen_cpu = cv2.resize(imagen_cpu, (rect_width, rect_height))
          frame[rect_cpu_y1:rect_cpu_y2, rect_cpu_x1:rect_cpu_x2] = imagen_cpu
      fuente = cv2.FONT_HERSHEY_SIMPLEX

      jugador_text = "Jugador: " + nombre_jugada_jugador
      jugador_font = cv2.FONT_HERSHEY_SIMPLEX
      jugador_font_scale = 0.8
      jugador_thickness = 2
      jugador_text_size = cv2.getTextSize(jugador_text, jugador_font, jugador_font_scale, jugador_thickness)[0]
      jugador_text_x = rect_player_x1 + (rect_width - jugador_text_size[0]) // 2  
      jugador_text_y =  bar_height // 2 + jugador_text_size[1] // 2
      cv2.putText(frame, jugador_text, (jugador_text_x, jugador_text_y), jugador_font, jugador_font_scale, (0, 255, 0), jugador_thickness, cv2.LINE_AA)

      cpu_text = "CPU: " + nombre_jugada_cpu
      cpu_text_size = cv2.getTextSize(cpu_text, jugador_font, jugador_font_scale, jugador_thickness)[0]
      cpu_text_x = rect_cpu_x1 + (rect_width - cpu_text_size[0]) // 2  
      cpu_text_y = bar_height // 2 + cpu_text_size[1] // 2  
      cv2.putText(frame, cpu_text, (cpu_text_x, cpu_text_y), jugador_font, jugador_font_scale, (0, 0, 255), jugador_thickness, cv2.LINE_AA)

      stats_text = "V - E - D"
      stats_font = cv2.FONT_HERSHEY_SIMPLEX
      stats_font_scale = 0.8
      stats_thickness = 2

      stats_text_size = cv2.getTextSize(stats_text, stats_font, stats_font_scale, stats_thickness)[0]
      stats_text_x = rect_player_x1 + (rect_width - stats_text_size[0]) // 2
      stats_text_y = rect_player_y2 + 30  
      cv2.putText(frame, stats_text, (stats_text_x, stats_text_y), stats_font, stats_font_scale, (255, 255, 255), stats_thickness, cv2.LINE_AA)

      stats_values = f"{victorias} - {empates} - {derrotas}"
      stats_values_size = cv2.getTextSize(stats_values, stats_font, stats_font_scale, stats_thickness)[0]
      stats_values_x = rect_player_x1 + (rect_width - stats_values_size[0]) // 2 
      stats_values_y = stats_text_y + 30  
      cv2.putText(frame, stats_values, (stats_values_x, stats_values_y), stats_font, stats_font_scale, (255, 255, 255), stats_thickness, cv2.LINE_AA)

      if nombre_ganador == "Ganaste" and ciclos > 0:
        resultado_text = "Ganaste"
        color = (0, 255, 0) 
      elif nombre_ganador == "Perdiste" and ciclos > 0:
        resultado_text = "Perdiste"
        color = (0, 0, 255)
      elif nombre_ganador == "Empate" and ciclos > 0:
        resultado_text = "Empate"
        color = (255, 255, 0)  
      else:
        resultado_text = "Esperando..."
        color = (255, 255, 255)  

      resultado_font = cv2.FONT_HERSHEY_SIMPLEX
      resultado_font_scale = 1
      resultado_thickness = 2
      resultado_text_size = cv2.getTextSize(resultado_text, resultado_font, resultado_font_scale, resultado_thickness)[0]
      resultado_text_x = (width - resultado_text_size[0]) // 2 
      resultado_text_y = height - bar_height - 20

      cv2.putText(frame, resultado_text, (resultado_text_x, resultado_text_y), resultado_font, resultado_font_scale, color, resultado_thickness, cv2.LINE_AA)


    else:
        mensaje = "Pulgar arriba para comenzar"
        font_scale = 1.5 
        thickness = 3 
        text_size = cv2.getTextSize(mensaje, font, font_scale, thickness)[0]
        text_x = (width - text_size[0]) // 2 
        text_y = bar_height // 2 + text_size[1] // 2 
        cv2.putText(frame, mensaje, (text_x, text_y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

        if victorias > 0 or derrotas > 0 or empates > 0:
            cv2.putText(frame, "ULTIMA PUNTUACION", (310, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (180, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(frame, "Victorias - Empates - Derrotas", (340, 200), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(frame, str(victorias) + " - " + str(empates) + " - " + str(derrotas), (340, 250), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2, cv2.LINE_AA)

        if time.time() - start_time > 1:
            cv2.imwrite('start.jpg', roi)
            start_time = time.time()

            movimientoStartID = choice([0, 4]) 
            if movimientoStartID == 4:
                victorias = 0
                derrotas = 0
                empates = 0
                working = True
                ciclos = 0

    cv2.imshow("Piedra, Papel o Tijeras", frame)

    key = cv2.waitKey(10)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()