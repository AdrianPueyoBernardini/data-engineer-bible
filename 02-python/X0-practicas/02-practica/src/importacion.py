import csv
import json

from lectura import leer_csv, leer_json, RUTA_CSV, RUTA_JSON
from validacion import validar_ruta, validar_plan

DIRECTORIO_PROYECTO = RUTA_CSV.parent.parent
DIRECTORIO_SALIDA = DIRECTORIO_PROYECTO / "salida"

RUTA_ESTADO = DIRECTORIO_SALIDA / "estado.json"
RUTA_INFORME = DIRECTORIO_SALIDA / "informe.json"

def clasificar_lote(
    filas,
    registros_anteriores,
    campo_id,
    archivo,
    validador
):
    # Índice de registros que ya están guardados.
    # La clave es el identificador de cada registro.
    registros_por_id = {}

    for registro in registros_anteriores:
        clave = registro[campo_id]

        if clave in registros_por_id:
            raise ValueError(
                f"Identificador duplicado en el estado anterior: {clave}"
            )

        registros_por_id[clave] = registro

    resumen = {
        "procesados": 0,
        "nuevos": 0,
        "duplicados": 0,
        "conflictos": 0,
        "rechazados": 0
    }

    incidencias = []

    # Recorremos las filas de la nueva importación.
    for numero, fila in enumerate(filas, start=1):
        resumen["procesados"] += 1

        # PRIMERO: validar y normalizar.
        registro, motivo = validador(fila)

        if motivo is not None:
            resumen["rechazados"] += 1

            clave = (
                fila.get(campo_id)
                if isinstance(fila, dict)
                else None
            )

            incidencias.append({
                "archivo": archivo,
                "registro": numero,
                "clave": clave,
                "motivo": motivo
            })

            continue

        # SEGUNDO: clasificar por identidad y contenido.
        clave = registro[campo_id]
        anterior = registros_por_id.get(clave)

        if anterior is None:
            # No existía: incorporamos el nuevo registro.
            registros_por_id[clave] = registro
            resumen["nuevos"] += 1

        elif registro == anterior:
            # Misma identidad y mismo contenido normalizado.
            resumen["duplicados"] += 1

            incidencias.append({
                "archivo": archivo,
                "registro": numero,
                "clave": clave,
                "motivo": "DUPLICADO_IDENTICO"
            })

        else:
            # Misma identidad, pero contenido diferente.
            # No reemplazamos el registro anterior.
            resumen["conflictos"] += 1

            incidencias.append({
                "archivo": archivo,
                "registro": numero,
                "clave": clave,
                "motivo": "CONFLICTO_CONTENIDO_DISTINTO"
            })

    return {
        "estado": list(registros_por_id.values()),
        "resumen": resumen,
        "incidencias": incidencias
    }


def cargar_estado(ruta_estado):
    """Carga el estado anterior o devuelve uno vacío
    si todavía no existe.
    """

    if not ruta_estado.exists():
        return {
            "rutas": [],
            "planes": []
        }

    with ruta_estado.open("r", encoding="utf-8") as archivo:
        estado = json.load(archivo)

    # Un estado existente debe tener la estructura esperada.
    if not isinstance(estado, dict):
        raise ValueError("El estado debe ser un objeto JSON")

    for entidad in ("rutas", "planes"):
        if not isinstance(estado.get(entidad), list):
            raise ValueError(
                f"El estado no contiene una lista válida de {entidad}"
            )

    # Comprobación básica de la estructura de cada registro.
    for entidad, campo_id in (
        ("rutas", "id_ruta"),
        ("planes", "id_plan")
    ):
        for numero, registro in enumerate(
            estado[entidad], start=1
        ):
            if (
                not isinstance(registro, dict)
                or not isinstance(registro.get(campo_id), str)
            ):
                raise ValueError(
                    f"Registro {numero} inválido en estado: {entidad}"
                )

    return {
        "rutas": estado["rutas"],
        "planes": estado["planes"]
    }

def guardar_json(ruta_archivo, datos):
    """Guarda los datos en un archivo JSON legible."""

    ruta_archivo.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with ruta_archivo.open(
        "w",
        encoding="utf-8"
    ) as archivo:
        json.dump(
            datos,
            archivo,
            ensure_ascii=False,
            indent=2,
            allow_nan=False
        )
        archivo.write("\n")


def ejecutar_importacion():

    # FASE 1: cargar el estado anterior y leer las entradas.
    # Todavía no escribimos ningún archivo de salida.
    try:
        estado_anterior = cargar_estado(RUTA_ESTADO)

        filas_rutas = leer_csv(RUTA_CSV)
        filas_planes = leer_json(RUTA_JSON)

        if not isinstance(filas_planes, list):
            raise ValueError(
                "planes.json debe contener una lista de planes"
            )

    except (
        OSError,
        UnicodeError,
        csv.Error,
        json.JSONDecodeError,
        ValueError
    ) as error:
        print(f"ERROR DE LECTURA: {error}")
        print("No se ha guardado una nueva importación.")
        return

    # FASE 2: clasificar las rutas frente al estado anterior.
    try:
        resultado_rutas = clasificar_lote(
            filas=filas_rutas,
            registros_anteriores=estado_anterior["rutas"],
            campo_id="id_ruta",
            archivo="rutas.csv",
            validador=validar_ruta
        )

        # Las referencias de los planes pueden apuntar tanto
        # a rutas anteriores como a las incorporadas ahora.
        ids_rutas_validas = {
            ruta["id_ruta"]
            for ruta in resultado_rutas["estado"]
        }

        # FASE 3: clasificar los planes.
        resultado_planes = clasificar_lote(
            filas=filas_planes,
            registros_anteriores=estado_anterior["planes"],
            campo_id="id_plan",
            archivo="planes.json",
            validador=lambda fila: validar_plan(
                fila, ids_rutas_validas
            )
        )

    except (KeyError, TypeError, ValueError) as error:
        print(f"ERROR AL PROCESAR LOS DATOS: {error}")
        print("No se ha guardado una nueva importación.")
        return

    # FASE 4: construir el estado candidato.
    estado_candidato = {
        "rutas": resultado_rutas["estado"],
        "planes": resultado_planes["estado"]
    }

    # FASE 5: construir el informe de esta ejecución.
    informe = {
        "rutas": {
            "archivo": "rutas.csv",
            **resultado_rutas["resumen"]
        },
        "planes": {
            "archivo": "planes.json",
            **resultado_planes["resumen"]
        },
        "incidencias": (
            resultado_rutas["incidencias"]
            + resultado_planes["incidencias"]
        )
    }

    # FASE 6: guardar las salidas.
    try:
        guardar_json(RUTA_ESTADO, estado_candidato)
        guardar_json(RUTA_INFORME, informe)

    except (OSError, TypeError, ValueError) as error:
        print(f"ERROR AL GUARDAR LOS RESULTADOS: {error}")
        print("No se puede confirmar la importación.")
        return

    # FASE 7: mostrar el resultado.
    print("Importación finalizada.")

    print("\nRUTAS")
    print(resultado_rutas["resumen"])

    print("\nPLANES")
    print(resultado_planes["resumen"])

    print(f"\nEstado guardado en: {RUTA_ESTADO}")
    print(f"Informe guardado en: {RUTA_INFORME}")


if __name__ == "__main__":
    ejecutar_importacion()
