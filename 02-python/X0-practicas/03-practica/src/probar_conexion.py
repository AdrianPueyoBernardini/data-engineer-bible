from db import abrir_conexion

conn = abrir_conexion()

try:
    with conn.cursor() as cur:
        cur.execute("SELECT 1")
        print("Resultado:", cur.fetchone())
finally:
    conn.close()