import math
import re
from datetime import date

#CAMPS PARA VALIDAR LA RUTA (A)
CAMPOS_RUTA = ["id_ruta", "ruta", "distancia_km", "desnivel_m", "valle", "dificultad"]
DIFICULTADES = {"fácil", "moderada", "difícil", "muy difícil"}
PATRON_ID_RUTA = re.compile(r"^R\d{2,}$")

#CAMPOS PARA VALIDAR EL PLAN (B)
CAMPOS_PLAN = ["id_plan", "id_ruta", "fecha_inicio", "fecha_fin", "estado"]
ESTADOS_PLAN = {"planificado", "realizado"}
PATRON_ID_PLAN = re.compile(r"^P\d{2,}$")
PATRON_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")

#CON ESTO VALIDO A (EL CSV)
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
    
    desnivel_texto = limpio["desnivel_m"]

    if desnivel_texto == "—":
        desnivel = None
    else:
        try:
            desnivel = int(desnivel_texto)
        except ValueError:
            return None, (
                f"TIPO_INCORRECTO: desnivel_m = '{desnivel_texto}'"
            )

    # FASE 3: rangos y valores admitidos.
    if not math.isfinite(distancia) or distancia <= 0:  # float acepta "nan" e "inf"
        return None, f"RANGO: distancia_km = {limpio['distancia_km']}"
    if desnivel is not None and desnivel < 0:
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

#CON ESTO VALIDO B (EL JSON)
def validar_plan(fila, ids_rutas_validas):
    """Valida un plan.
    Devuelve (registro_normalizado, None) o (None, motivo).
    """

    # FASE 0: comprobar que el registro tiene la estructura esperada
    if not isinstance(fila, dict):
        return None, "ESTRUCTURA_INVALIDA: el plan debe ser un objeto JSON"

    # FASE 1: campos obligatorios
    for campo in CAMPOS_PLAN:
        valor = fila.get(campo)

        if valor is None or (
            isinstance(valor, str) and not valor.strip()
        ):
            return None, f"CAMPO_OBLIGATORIO: {campo}"

    # FASE 2: tipos
    # En JSON no convertimos automáticamente números a cadenas.
    for campo in CAMPOS_PLAN:
        if not isinstance(fila[campo], str):
            return None, f"TIPO_INCORRECTO: {campo} debe ser texto"

    # Normalizamos quitando solo espacios exteriores.
    limpio = {
        campo: fila[campo].strip()
        for campo in CAMPOS_PLAN
    }

    # FASE 3: valores admitidos
    if limpio["estado"] not in ESTADOS_PLAN:
        return None, f"DOMINIO: estado = '{limpio['estado']}'"

    # FASE 3: comprobar que las fechas existen realmente
    fechas = {}

    for campo in ("fecha_inicio", "fecha_fin"):
        texto_fecha = limpio[campo]

        if not PATRON_FECHA.fullmatch(texto_fecha):
            return None, (
                f"FECHA_INVALIDA: {campo} debe usar AAAA-MM-DD"
            )

        try:
            fechas[campo] = date.fromisoformat(texto_fecha)
        except ValueError:
            return None, (
                f"FECHA_INVALIDA: {campo} no es una fecha real"
            )

    # FASE 3: coherencia entre las fechas
    if fechas["fecha_fin"] < fechas["fecha_inicio"]:
        return None, "FECHAS_INCOHERENTES: fecha_fin es anterior a fecha_inicio"

    # FASE 4: comprobar la referencia a la entidad A
    if limpio["id_ruta"] not in ids_rutas_validas:
        return None, (
            f"REFERENCIA_INEXISTENTE: id_ruta = '{limpio['id_ruta']}'"
        )

    # FASE 5: validar el formato de la identidad
    if not PATRON_ID_PLAN.fullmatch(limpio["id_plan"]):
        return None, f"DOMINIO: id_plan = '{limpio['id_plan']}'"

    # Si todo es correcto, devolvemos el registro normalizado.
    return {
        "id_plan": limpio["id_plan"],
        "id_ruta": limpio["id_ruta"],
        "fecha_inicio": limpio["fecha_inicio"],
        "fecha_fin": limpio["fecha_fin"],
        "estado": limpio["estado"]
    }, None


#Pongo esto para contabilizar las válidas y no válidas
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