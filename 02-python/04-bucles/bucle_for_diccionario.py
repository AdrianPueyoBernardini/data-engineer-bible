mi_diccionario = {

    "Nombre":"Adrian",
      "Edad":24
      
      }

for i in mi_diccionario:
    print(i, mi_diccionario[i])

#lo mismo en ambas opciones

for dato,valor in mi_diccionario.items():
    print(dato, valor)
