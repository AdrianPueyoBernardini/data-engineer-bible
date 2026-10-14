import math
import re

CAMPOS_RUTA = ["id_ruta", "ruta", "distancia_km", "desnivel_m", "valle", "dificultad"]
DIFICULTADES = {"fácil", "moderada", "difícil", "muy difícil"}
PATRON_ID_RUTA = re.compile(r"^R\d{2,}$")


def validar_ruta(fila):
    """Valida y normaliza una fila de A. Devuelve (registro, None) o (None, motivo)."""

    # FASE 1: obligatorios. Un valor None (celda ausente) o "" (vacío/solo espacios) falla.
    for campo in CAMPOS_RUTA:
        if not str(fila.get(campo) or "").strip():
            return None, f"CAMPO_OBLIGATORIO: {campo}"

    # Recortamos espacios SOLO en los extremos; el contenido no se toca.
    limpio = {campo: str(fila[campo]).strip() for campo in CAMPOS_RUTA}

    # FASE 2: tipos. En CSV todo llega como texto: aquí lo convertimos según el diccionario.
    try:
        distancia = float(limpio["distancia_km"].replace(",", "."))
    except ValueError:
        return None, f"TIPO_INCORRECTO: distancia_km = '{limpio['distancia_km']}'"

    try:
        desnivel = int(limpio["desnivel_m"])  # int("12,5") falla: no es un entero
    except ValueError:
        return None, f"TIPO_INCORRECTO: desnivel_m = '{limpio['desnivel_m']}'"

    # FASE 3: rangos y valores admitidos.
    if not math.isfinite(distancia) or distancia <= 0:  # float acepta "nan" e "inf"
        return None, f"RANGO: distancia_km = {limpio['distancia_km']}"
    if desnivel < 0:
        return None, f"RANGO: desnivel_m = {desnivel}"
    if not PATRON_ID_RUTA.match(limpio["id_ruta"]):
        return None, f"DOMINIO: id_ruta = '{limpio['id_ruta']}'"
    if limpio["dificultad"] not in DIFICULTADES:
        return None, f"DOMINIO: dificultad = '{limpio['dificultad']}'"

    # Registro normalizado
    return {
        "id_ruta": limpio["id_ruta"],
        "ruta": limpio["ruta"],
        "distancia_km": distancia,
        "desnivel_m": desnivel,
        "valle": limpio["valle"],
        "dificultad": limpio["dificultad"],
    }, None

if __name__ == "__main__":
    from lectura import leer_csv, RUTA_CSV

    validas, rechazadas = 0, 0
    for numero, fila in enumerate(leer_csv(RUTA_CSV), start=1):
        registro, motivo = validar_ruta(fila)
        if motivo is None:
            validas += 1
        else:
            rechazadas += 1
            print(f"registro {numero}: {motivo}")
    print(f"válidas={validas}, rechazadas={rechazadas}")
    print(validar_ruta({"id_ruta": "R99", "ruta": "Prueba", "distancia_km": "1,5",
                        "desnivel_m": "10", "valle": "X", "dificultad": "fácil"}))