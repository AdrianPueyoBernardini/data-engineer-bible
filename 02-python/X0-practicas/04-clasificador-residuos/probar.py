import numpy as np
import tensorflow as tf

# Lista con los contenedores ordenados alfabéticamente (como los lee Keras)
clases = ['amarillo', 'azul', 'gris', 'marron', 'verde']

# 1. Cargar el modelo guardado
modelo = tf.keras.models.load_model("clasificador_residuos.h5")

def predecir_foto(ruta_imagen):
    # Cargar y redimensionar la imagen a 224x224
    img = tf.keras.utils.load_img(ruta_imagen, target_size=(224, 224))
    img_array = tf.keras.utils.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Crear un lote de tamaño 1

    # Hacer la predicción
    predicciones = modelo.predict(img_array)
    indice_ganador = np.argmax(predicciones[0])
    porcentaje = 100 * np.max(predicciones[0])

    contenedor = clases[indice_ganador]
    print(f"\nFoto: {ruta_imagen}")
    print(f"Resultado: ¡Va al contenedor {contenedor.upper()}! (Seguridad: {porcentaje:.2f}%)")

# Ejemplo de uso:
# Cambia 'foto_test.jpg' por el nombre de la foto que quieras probar
predecir_foto("foto_test.jpg")