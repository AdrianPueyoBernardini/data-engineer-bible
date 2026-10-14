import json
import csv
from pathlib import Path


DIRECTORIO_PADRE = Path(__file__).resolve().parent.parent
RUTA_CSV = DIRECTORIO_PADRE / "entrada" / "rutas.csv"
RUTA_JSON = DIRECTORIO_PADRE / "entrada" / "planes.json"



#Leemos el csv y lo convertimos en una lista de diccionarios
#* dictreader, cada fila del csv se convierte en un diccionario
#* newline='' para evitar problemas con los saltos de línea en Windows
def leer_csv(ruta_archivo):
    datos = []
    with open(ruta_archivo, mode='r', encoding='utf-8', newline='') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            datos.append(fila)
    return datos

#Leemos el json y lo retornamos como lista
#json.load carga el archivo
def leer_json(ruta_archivo):
    with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return datos

#Validador de campos según cada una de las filas




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
