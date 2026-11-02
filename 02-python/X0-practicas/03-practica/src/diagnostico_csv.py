import csv
from importador import RUTAS_CSV, DELIMITADOR, CODIFICACION

print("Delimitador en uso:", repr(DELIMITADOR))
print("Archivo leído:", RUTAS_CSV)

with open(RUTAS_CSV, encoding=CODIFICACION, newline="") as f:
    lector = csv.DictReader(f, delimiter=DELIMITADOR)
    print("Columnas detectadas:", lector.fieldnames)
    print("Primera fila:", next(lector))