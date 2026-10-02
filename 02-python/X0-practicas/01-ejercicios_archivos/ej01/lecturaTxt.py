#Importamos pathlib para bsucar el archivo en la misma carpeta que el script
#encoding utf-8 para que lea correctamente los acentos y caracteres especiales
#para contar las lineas del txt se puede usar len(f.readlines()) pero hay que abrir el archivo de nuevo para leerlo
from pathlib import Path

def lectura_txt():
    archivo = Path(__file__).with_name("poema.txt")
    contadorLineas = 0

    with open(archivo, "r", encoding="utf-8") as f:
        # Leemos el fichero .txt
        print(f.read())

        # Reseteamos el puntero del archivo al principio para poder contar las lineas
        #con el for contamos cada una de las lineas
        f.seek(0)
        for linea in f:
            contadorLineas += 1

        #Volvemos a resetear el puntero
        #leemos el texto y creamos un array con todas las palabras del texto usando split()
        f.seek(0)
        texto = f.read()
        palabras = texto.split()

        #Vamos a contar ahora caracteres
        caracteres=len(texto)

        f.close()

        

    print("El archivo contiene: " + str(contadorLineas) + " lineas")
    print("El archivo contiene: " + str(len(palabras)) + " palabras")
    print("El archivo contiene: " + str(caracteres) + " caracteres")


lectura_txt()

