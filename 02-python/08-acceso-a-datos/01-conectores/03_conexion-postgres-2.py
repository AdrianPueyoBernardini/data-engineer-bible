import psycopg

# PASO 1: Conectar con PostgreSQL
with psycopg.connect(
    host="localhost",      # Marcamos localhost
    dbname="postgres",     # Nombre de nuestra base de datos (NO TABLA)
    user="odoo",           # Nombre del usuario que conecta a la bbdd
    password="odoopwd"     # Contraseña de acceso
) as conn:
    # PASO 2 y 3: Creamos la tabla e insertamos el registro (evitando fallo si ya existe)
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS salas_prueba_2 (
                id INTEGER PRIMARY KEY,
                nombre VARCHAR(40) NOT NULL
            )
        """)
        cursor.execute("""
            INSERT INTO salas_prueba_2 (id, nombre)
            VALUES (1, 'arte')
            ON CONFLICT (id) DO NOTHING
        """)

    # PASO 4: Consultamos usando un segundo cursor sobre la misma conexión
    with conn.cursor() as cursor_2:
        cursor_2.execute("""
            SELECT id, nombre
            FROM salas_prueba_2
        """)
        filas = cursor_2.fetchall()
        print("Filas encontradas:", filas)

print("Primera conexión cerrada.")