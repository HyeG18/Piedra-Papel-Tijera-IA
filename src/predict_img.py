import os
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from rembg import remove
from PIL import Image
# Ruta al modelo guardado
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../models/piedra_papel_tijera_model.keras"))

# Dimensiones esperadas de las imágenes por el modelo
IMG_HEIGHT = 20
IMG_WIDTH = 30

# Etiquetas de las clases
CLASS_LABELS = ["Paper", "Rock", "Scissors", "Nothing"]

def load_trained_model(model_path):
    """Carga el modelo entrenado desde la ruta especificada."""
    try:
        print(f"Intentando cargar el modelo desde: {os.path.abspath(model_path)}")
        model = load_model(model_path)
        print(f"Modelo cargado correctamente desde: {model_path}")
        return model
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        exit(1)


def preprocess_image(image_path):
    """Preprocesa una imagen para que sea compatible con el modelo."""
    try:
        # Cargar la imagen
        with Image.open(image_path) as img:
            # Remover el fondo
            img_no_bg = remove(img)

            # Convertir a escala de grises
            img_gray = img_no_bg.convert("L")

            # Redimensionar la imagen
            img_resized = img_gray.resize((IMG_WIDTH, IMG_HEIGHT))

            # Normalizar los valores de los píxeles
            img_array = np.array(img_resized) / 255.0
            img_array = np.expand_dims(img_array, axis=(0, -1))  # Añadir dimensiones para el batch
            return img_array
    except Exception as e:
        print(f"Error al procesar la imagen '{image_path}': {e}")
        exit(1)

def predict_image(model, image_path):
    """Realiza una predicción sobre una imagen y muestra las probabilidades."""
    img_array = preprocess_image(image_path)
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    probabilities = predictions[0]

    print(f"\nPredicción para la imagen '{image_path}':")
    print(f"Clase predicha: {CLASS_LABELS[predicted_class]}")
    print("Probabilidades:")
    for label, prob in zip(CLASS_LABELS, probabilities):
        print(f"  {label}: {prob:.4f}")

def main():
    # Ruta a la carpeta predict y a la imagen que se desea predecir
    PREDICT_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "predict"))
    IMAGE_NAME = "nadaYo2.jpg"  # Cambia esto al nombre de tu imagen
    IMAGE_PATH = os.path.join(PREDICT_FOLDER, IMAGE_NAME)

    # Verificar si la imagen existe
    if not os.path.exists(IMAGE_PATH):
        print(f"La imagen '{IMAGE_PATH}' no existe.")
        exit(1)

    # Cargar el modelo
    model = load_trained_model(MODEL_PATH)

    # Realizar la predicción
    predict_image(model, IMAGE_PATH)

if __name__ == "__main__":
    main()