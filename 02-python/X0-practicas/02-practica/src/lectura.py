from pathlib import Path
import csv
import json

#Sacamos la ruta principal:
#.resolve() me da la ruta absoluta completa
#.parent para ir al directorio padre
directorio_principal = Path(__file__).resolve().parent.parent
ruta_csv = directorio_principal / "entrada" / "rutas.csv"
planes_json = directorio_principal / "entrada" / "planes.json"

#Leemos el CSV
#Para la lectura de los csv es necesario el newline=''
def lectura_rutas_csv():
    with open(ruta_csv, "r", encoding="utf-8", newline='') as f:
            dictreader = csv.DictReader(f)
            filas = []
            for fila in dictreader:
                filas.append(fila)
    return filas

#Leemos el json
def lectura_planes_json():
     with open(planes_json, "r", encoding="utf-8") as f:
          return json.load(f)

#for fila in lectura_rutas_csv():
#     print(fila)
#print(len(lectura_rutas_csv()))

#print(lectura_planes_json())
for fila in lectura_planes_json():
     print(fila)