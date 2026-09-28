import os
from pathlib import Path
import shutil

def crear_carpetas():
    #con path(__file__).parent obtenemos la ruta donde se encuentra el script, es decir, el padre
    ruta = Path(__file__).parent
    ruta_muestras = Path(__file__).parent.with_name("muestras")
    ruta_archivo = Path(__file__).with_name("archivo")
    print(ruta)
    print(ruta_muestras)
    print(ruta_archivo)

    #De esta forma asignamos la ruta y creamos las carpetas
    #Con un if(not os.path.exists()) nos aseguramos si existe, si no existe la creamos con os.mkdir()
    if(not os.path.exists(ruta/"copias")):
        os.mkdir(ruta/"copias")
    if(not os.path.exists(ruta/"archivo")):
        os.mkdir(ruta/"archivo")

    #Con shutil podemos copiar todo el arbol de archuvos de la ruta.
    shutil.copytree(ruta_muestras, ruta_archivo, dirs_exist_ok=True)


crear_carpetas()