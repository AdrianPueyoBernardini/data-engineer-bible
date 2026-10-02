from pathlib import Path

def escribe_txt():
    #lectura de archivo en librería
    archivo = Path(__file__).with_name("titulos.txt")

    #sobreescritura en el archivo
    with open(archivo, "w", encoding="utf-8") as f:

        f.write("1. El Quijote\n")
        f.write("2. El Lazarillo de Tormes\n")
        f.write("3. La Celestina\n")
        f.write("4. El Cantar del Mío Cid\n")
        f.write("5. La Regenta\n")
        f.write("6. Fortunata y Jacinta\n")
        f.write("7. Los Pazos de Ulloa\n")
        f.write("8. El árbol de la ciencia\n")
        f.write("9. La familia de Pascual Duarte\n")
        f.close()

    #Escritura de una línea al final del archivo
    with open(archivo, "a", encoding="utf-8") as f:
        f.write(" Ejecución realizada")
        f.close()
        
    #lectura
    with open(archivo, "r", encoding="utf-8") as f:
        f.seek(0) 
        print(f.read())
        f.close()

escribe_txt()