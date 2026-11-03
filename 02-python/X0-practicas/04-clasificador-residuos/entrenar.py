import tensorflow as tf
from tensorflow.keras import layers, models

# 1. Configuración básica
ANCHO = 224
ALTO = 224
TAMANO_LOTE = 16  # Procesa las imágenes en grupos de 16
CARPETA_DATOS = "datos_residuos"

# 2. Cargar imágenes de las 5 carpetas
# Separa automáticamente el 80% para entrenar y el 20% para validar
print("Cargando datos de entrenamiento...")
datos_entreno = tf.keras.utils.image_dataset_from_directory(
    CARPETA_DATOS,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(ALTO, ANCHO),
    batch_size=TAMANO_LOTE
)

print("Cargando datos de validación...")
datos_validacion = tf.keras.utils.image_dataset_from_directory(
    CARPETA_DATOS,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(ALTO, ANCHO),
    batch_size=TAMANO_LOTE
)

# Guardar los nombres de los contenedores
nombres_clases = datos_entreno.class_names
print("Clases detectadas:", nombres_clases)

# Optimización para que la carga sea rápida
datos_entreno = datos_entreno.cache().shuffle(1000).prefetch(buffer_size=tf.data.AUTOTUNE)
datos_validacion = datos_validacion.cache().prefetch(buffer_size=tf.data.AUTOTUNE)

# 3. Crear el modelo usando una red neuronal preentrenada (MobileNetV2)
# Esto ayuda a que aprenda con pocas fotos y funcione muy bien
base_model = tf.keras.applications.MobileNetV2(
    input_shape=(ALTO, ANCHO, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False  # Congelamos la base para no borrar lo que ya sabe

# Ensamblamos el clasificador
modelo = models.Sequential([
    # Escalamos los píxeles al rango que necesita MobileNetV2 (-1 a 1)
    layers.Rescaling(1./127.5, offset=-1, input_shape=(ALTO, ANCHO, 3)),
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dropout(0.2),  # Evita que el modelo memorice las fotos exactas
    layers.Dense(len(nombres_clases), activation='softmax')  # Salida para 5 contenedores
])

# 4. Compilar el modelo
modelo.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(),
    metrics=['accuracy']
)

# 5. Entrenar la red neuronal
print("\n¡Empieza el entrenamiento!")
modelo.fit(
    datos_entreno,
    validation_data=datos_validacion,
    epochs=10  # Número de pasadas completas a tus fotos
)

# 6. Guardar el modelo entrenado
modelo.save("clasificador_residuos.h5")
print("\n¡Modelo guardado con éxito como 'clasificador_residuos.h5'!")