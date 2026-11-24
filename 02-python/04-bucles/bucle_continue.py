contador = 0
lista_nombres = {"Adri", "Juan", "Miguel"}

while contador<=10:
    if contador==5:
        contador+=1
        continue
    print(contador)
    contador+=1

for i in lista_nombres:

    if i == "Juan":
        break

    print(i)