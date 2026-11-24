# ----------------------INSTALACION-----------------------------------
# Primero instalaremos sqlalquemy para la practica, dotenv y psycopg, todo en terminal:
# python -m pip install "psycopg[binary]" "sqlalchemy>=2.0,<3" python-dotenv
# ----------------------DATOS/INFO-----------------------------------
# POSTGRESQL NO es embebido

# Adaptador de BBDD para postgresql/python
import psycopg

# Abrimos conexión a la base de datos
with psycopg.connect(

    host="localhost",      #Marcamos localhost
    dbname="postgres",     #Nombre de nuestra base de datos (NO TABLA)
    user="postgres",       #Nombre del usuario que conecta a la bbdd
    password="postgres"    #Contraseña de acceso
) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT 1 + 1")
        resultado = cursor.fetchone()
        print(resultado)