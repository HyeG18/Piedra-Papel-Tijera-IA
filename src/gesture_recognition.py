import cv2

def countdown_and_capture(cap, roi_coords, mirror_effect):
    """Realiza un conteo regresivo y toma una foto de una región específica."""
    x, y, w, h = roi_coords  # Coordenadas del recuadro (x, y, ancho, alto)

    for i in range(3, 0, -1):
        print(f"Preparado... {i}")
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo leer el fotograma.")
            return None

        # Aplica el efecto de espejo si está activado
        if mirror_effect:
            frame = cv2.flip(frame, 1)

        # Dibuja las barras negras
        height, width, _ = frame.shape
        cv2.rectangle(frame, (0, 0), (width, 100), (0, 0, 0), -1)  # Barra superior
        cv2.rectangle(frame, (0, height - 100), (width, height), (0, 0, 0), -1)  # Barra inferior

        # Dibuja el recuadro en el fotograma
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Dibuja la línea divisora en el medio de la pantalla
        cv2.line(frame, (width // 2, 100), (width // 2, height - 100), (255, 0, 0), 2)

        # Calcula el tamaño del texto "Player"
        player_text = "Player"
        player_text_size = cv2.getTextSize(player_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        player_text_x = x + (w - player_text_size[0]) // 2  # Centra horizontalmente
        cv2.putText(frame, player_text, (player_text_x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Calcula el tamaño del texto "CPU"
        cpu_text = "CPU"
        cpu_text_size = cv2.getTextSize(cpu_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        cpu_text_x = (width - x - w) + (w - cpu_text_size[0]) // 2  # Centra horizontalmente
        cv2.putText(frame, cpu_text, (cpu_text_x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow('Camera', frame)
        cv2.waitKey(1000)  # Espera 1 segundo entre cada número

    # Captura el fotograma final
    ret, frame = cap.read()
    if ret:
        # Aplica el efecto de espejo si está activado
        if mirror_effect:
            frame = cv2.flip(frame, 1)

        # Recorta la región de interés (ROI)
        roi = frame[y:y + h, x:x + w]
        cv2.imwrite('gesture.jpg', roi)
        print("Foto tomada y guardada como 'gesture.jpg'")
        return roi
    else:
        print("Error: No se pudo capturar la imagen.")
        return None

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara.")
        return

    # Coordenadas del recuadro (x, y, ancho, alto)
    roi_coords = (200, 200, 300, 300)  # Cambia estos valores según tu necesidad
    mirror_effect = True

    print("=== Piedra, Papel o Tijera ===")
    print("Presiona 's' para iniciar el juego. Presiona 'q' para salir.")
    print("Presiona 'm' para alternar el efecto de espejo.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo leer el fotograma.")
            break

        # Aplica el efecto de espejo si está activado
        if mirror_effect:
            frame = cv2.flip(frame, 1)

        # Dibuja las barras negras
        height, width, _ = frame.shape
        cv2.rectangle(frame, (0, 0), (width, 100), (0, 0, 0), -1)  # Barra superior
        cv2.rectangle(frame, (0, height - 100), (width, height), (0, 0, 0), -1)  # Barra inferior

        # Dibuja el recuadro en la ventana de la cámara
        x, y, w, h = roi_coords
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Dibuja la línea divisora en el medio de la pantalla
        cv2.line(frame, (width // 2, 100), (width // 2, height - 100), (255, 0, 0), 2)

        # Calcula el tamaño del texto "Player"
        player_text = "Player"
        player_text_size = cv2.getTextSize(player_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        player_text_x = x + (w - player_text_size[0]) // 2  # Centra horizontalmente
        cv2.putText(frame, player_text, (player_text_x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Calcula el tamaño del texto "CPU"
        cpu_text = "CPU"
        cpu_text_size = cv2.getTextSize(cpu_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        cpu_text_x = (width - x - w) + (w - cpu_text_size[0]) // 2  # Centra horizontalmente
        cv2.putText(frame, cpu_text, (cpu_text_x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        cv2.imshow('Camera', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Presiona 'q' para salir
            print("Saliendo del juego. ¡Hasta luego!")
            break
        elif key == ord('s'):  # Presiona 's' para iniciar el juego
            print("Iniciando el juego...")
            countdown_and_capture(cap, roi_coords, mirror_effect)
        elif key == ord('m'):  # Presiona 'm' para alternar el efecto de espejo
            mirror_effect = not mirror_effect
            print(f"Efecto de espejo {'activado' if mirror_effect else 'desactivado'}.")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()