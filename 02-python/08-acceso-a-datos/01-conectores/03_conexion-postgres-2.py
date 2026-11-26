import psycopg

# Abrimos conexión a la base de datos
with psycopg.connect(

    host="localhost",      #Marcamos localhost
    dbname="postgres",     #Nombre de nuestra base de datos (NO TABLA)
    user="odoo",          #Nombre del usuario que conecta a la bbdd
    password="odoopwd"    #Contraseña de acceso
) as conn:
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXIST salas_prueba (
                id INTEGER PRIMARY KEY,
            )
        """)
        resultado = cursor.fetchone()
        print(resultado)