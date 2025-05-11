from random import choice 
import cv2
import numpy as np
import time
import os
from predict_img import load_trained_model, preprocess_image

MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../models/piedra_papel_tijera_model.keras"))

# Cargar el modelo
model = load_trained_model(MODEL_PATH)

CLASS_MAP = {
    0: "Papel",
    1: "Piedra",
    2: "Tijeras",
    3: "Nada",
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

    rect_width = 350
    rect_height = 350
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
    cv2.rectangle(frame, (rect_cpu_x1, rect_cpu_y1), (rect_cpu_x2, rect_cpu_y2), (255, 255, 255), 2)

    roi = frame[rect_player_y1:rect_player_y2, rect_player_x1:rect_player_x2]

    if working:
        elapsed_time = time.time() - start_time

        # Mostrar el contador
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

        # Realizar la predicción solo una vez por ronda
        if elapsed_time > 4.5 and not prev_jugada:
            temp_image_path = "temp_gesture.jpg"
            cv2.imwrite(temp_image_path, roi)

            preprocessed_roi = preprocess_image(temp_image_path)
            predictions = model.predict(preprocessed_roi)
            movimientoID = np.argmax(predictions)
            nombre_jugada_jugador = mapeado(movimientoID)

            # Eliminar la imagen temporal
            os.remove(temp_image_path)

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

            prev_jugada = True  # Marcar que la jugada ya se realizó

        # Reiniciar el ciclo después de mostrar el resultado
        if elapsed_time > 6:
            start_time = time.time()
            prev_jugada = False  # Permitir una nueva jugada

        # Mostrar resultados y estadísticas
        if nombre_jugada_cpu in ["Piedra", "Papel", "Tijera"]:
            ruta_imagen = f"imagenes/{nombre_jugada_cpu.lower()}.png"
            imagen_cpu = cv2.imread(ruta_imagen)

            if imagen_cpu is not None:
                imagen_cpu = cv2.resize(imagen_cpu, (rect_width, rect_height))
                frame[rect_cpu_y1:rect_cpu_y2, rect_cpu_x1:rect_cpu_x2] = imagen_cpu

        jugador_text = f"Jugador: {nombre_jugada_jugador}"
        cpu_text = f"CPU: {nombre_jugada_cpu}"
        stats_text = f"V - E - D: {victorias} - {empates} - {derrotas}"

        cv2.putText(frame, jugador_text, (10, 30), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, cpu_text, (10, 60), font, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, stats_text, (10, 90), font, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # Mostrar el mensaje de resultado (Ganaste, Perdiste, Empate)
        resultado_font_scale = 2
        resultado_thickness = 3
        resultado_text_size = cv2.getTextSize(nombre_ganador, font, resultado_font_scale, resultado_thickness)[0]
        resultado_text_x = (width - resultado_text_size[0]) // 2
        resultado_text_y = height - bar_height // 2 + resultado_text_size[1] // 2
        cv2.putText(frame, nombre_ganador, (resultado_text_x, resultado_text_y), font, resultado_font_scale, (0, 255, 255), resultado_thickness, cv2.LINE_AA)

    else:
        mensaje = "Presiona 'S' para comenzar"
        font_scale = 1.5
        thickness = 3
        text_size = cv2.getTextSize(mensaje, font, font_scale, thickness)[0]
        text_x = (width - text_size[0]) // 2
        text_y = bar_height // 2 + text_size[1] // 2
        cv2.putText(frame, mensaje, (text_x, text_y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

    cv2.imshow("Piedra, Papel o Tijeras", frame)

    key = cv2.waitKey(10)
    if key == ord('q'):
        break
    elif key == ord('s'):
        working = True
        start_time = time.time()

cap.release()
cv2.destroyAllWindows()