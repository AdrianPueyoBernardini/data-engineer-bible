# ----------------------INSTALACION-----------------------------------
# Primero instalaremos sqlalquemy para la practica, dotenv y psycopg, todo en terminal:
# python -m pip install "psycopg[binary]" "sqlalchemy>=2.0,<3" python-dotenv
# python -m pip install "psycopg[pool]"
# ----------------------DATOS/INFO-----------------------------------
# SQLite SI es embebido

#importamos la librería nativa sqlite3
import sqlite3
from pathlib import Path

# Ruta del archivo que almacenará la bbdd
ruta = Path(__file__).with_name("laboratorio.sqlite3")

# PASO 1: abrir la conexión
conexion = sqlite3.connect(ruta)

try:

# PASO 2: creamos la tabla
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS salas_prueba (
            id INTEGER PRIMARY KEY,
            nombre VARCHAR(30) NOT NULL
        )
    """)

# PASO 3: Insertar los datos a la tabla
    conexion.execute("""
        INSERT INTO salas_prueba (id, nombre)
        VALUES (22, 'Salas de clases')
    """)

# PASO 4: Insertar los datos a la tabla
    print("Cambios comiteados")
    conexion.commit()

finally:
# PASO 5: Cerramos la conexión
    conexion.close()
    print("Primer conexión cerrada")

# PASO 6: Abrimos de nuevo la conexión (la hemos cerrado)
conexion = sqlite3.connect(ruta)

# PASO 7: hacemos SELECT
try:
    select = conexion.execute("""
        SELECT * 
        FROM salas_prueba
    """).fetchone()

    print(select)

finally:
    conexion.close()

# -----------------------------NUEVO SELECT DE PRÁCTICA------------------

conexion = sqlite3.connect(ruta)

try:
    select2 = conexion.execute("""
        SELECT nombre
        FROM salas_prueba
        WHERE id > 10
    """).fetchone()

    print(select2)
finally:
    conexion.close
