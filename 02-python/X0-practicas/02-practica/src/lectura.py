import json
import csv
from pathlib import Path


DIRECTORIO_PADRE = Path(__file__).resolve().parent.parent
RUTA_CSV = DIRECTORIO_PADRE / "entrada" / "rutas.csv"
RUTA_JSON = DIRECTORIO_PADRE / "entrada" / "planes.json"
print(DIRECTORIO_PADRE)


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
def validar_registros(fila):


    #Validador del campo ruta
    try:
        ruta = fila['ruta']
    except KeyError:
        return None, "El campo 'ruta' no existe en la fila"
    #¿Es un número?
    if(str(ruta).isnumeric()):
        return None, "El valor 'ruta' es un número, se esperaba un string"


    #Validador del campo distancia_km
    try:
        distancia = fila['distancia_km']
    except KeyError:
        return None, "El campo 'distancia_km' no existe en la fila"
    #¿El campo se puede reemplazar por . ?
    try:
        float(str(distancia).replace(',', '.'))
    except ValueError:
        return None, "El campo 'distancia_km' no es un número, se esperaba un número"


    #Validador del campo desnivel_m
    try:
        desnivel = fila['desnivel_m']
    except KeyError:
        return None, "El campo 'desnivel_m' no existe en la fila"
    #¿El campo se puede reemplazar por . ?
    try:
        float(str(desnivel).replace(',', '.'))
    except ValueError:
        return None, "El campo 'desnivel_m' no es un número, se esperaba un número"


    #Validador del campo valle 
    try:
        valle = fila['valle']
    except KeyError:
        return None, "El campo 'valle' no existe en la fila"
    #Es un número
    if(str(valle).isnumeric()):
        return None, "El valor 'valle' es un número, se esperaba un string"
    
    return fila, None

mi_csv = leer_csv(RUTA_CSV)
print(validar_registros(mi_csv[0]))

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
