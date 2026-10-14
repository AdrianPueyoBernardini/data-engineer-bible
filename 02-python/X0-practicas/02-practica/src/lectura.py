import csv
import json

MAX_JSON_BYTES = 1_000_000  # Máximo: 1 MB


def leer_csv(ruta_archivo):
    """Lee el CSV fila a fila, sin acumularlo en una lista."""

    with open(
        ruta_archivo,
        mode="r",
        encoding="utf-8",
        newline=""
    ) as archivo:

        lector = csv.DictReader(archivo, strict=True)

        if not lector.fieldnames:
            raise csv.Error("El CSV no contiene una cabecera.")

        if len(lector.fieldnames) != len(set(lector.fieldnames)):
            raise csv.Error("El CSV contiene columnas duplicadas.")

        for fila in lector:
            # Más valores de los que permite la cabecera.
            if None in fila:
                raise csv.Error(
                    "Una fila tiene más campos que la cabecera."
                )

            yield fila


def leer_json(ruta_archivo, max_bytes=MAX_JSON_BYTES):
    """Lee el JSON completo, con un límite de tamaño."""

    if max_bytes <= 0:
        raise ValueError("El límite de tamaño debe ser positivo.")

    with open(ruta_archivo, mode="rb") as archivo:
        contenido = archivo.read(max_bytes + 1)

    if len(contenido) > max_bytes:
        raise ValueError(
            f"El archivo JSON supera el límite de {max_bytes} bytes."
        )

    texto = contenido.decode("utf-8")

    return json.loads(texto)
#--------------TEST-----------------
#LECTURA DE FILAS TOTALES DEL CSV
#print(len(leer_csv(RUTA_CSV)))

#LECTURA DEL CSV
#for f in leer_csv(RUTA_CSV):
#    print(f)

#LECTURA DEL JSON
#for f in leer_json(RUTA_JSON):
#    print(f)

#csv = leer_csv(RUTA_CSV)
#print(csv[0]['distancia_km'])
