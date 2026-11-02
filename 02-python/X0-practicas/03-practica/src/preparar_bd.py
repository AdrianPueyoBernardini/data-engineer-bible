from db import abrir_conexion, ROOT

ARCHIVOS = ["schema.sql", "procedimientos.sql"]

conn = abrir_conexion()
try:
    with conn.cursor() as cur:
        for nombre in ARCHIVOS:
            sql = (ROOT / "sql" / nombre).read_text(encoding="utf-8")
            cur.execute(sql)
            print("Aplicado:", nombre)
    conn.commit()
    print("Base preparada.")
finally:
    conn.close()