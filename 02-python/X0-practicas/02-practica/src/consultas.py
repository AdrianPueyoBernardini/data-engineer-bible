
def buscar_por_id(registros, campo_id, identificador):
    """Devuelve el registro que coincide con la identidad o None."""

    identificador = identificador.strip()

    for registro in registros:
        if registro.get(campo_id) == identificador:
            return registro

    return None


def filtrar_por_valor(registros, campo, valor):
    """Devuelve los registros cuyo campo coincide con el valor."""

    valor = str(valor).strip().casefold()

    resultados = []

    for registro in registros:
        dato = registro.get(campo)

        if dato is None:
            continue

        if str(dato).strip().casefold() == valor:
            resultados.append(registro)

    return resultados


def filtrar_rutas_por_distancia(rutas, distancia_minima):
    """Devuelve las rutas cuya distancia es igual o superior al mínimo."""

    resultados = []

    for ruta in rutas:
        distancia = ruta.get("distancia_km")

        if isinstance(distancia, (int, float)):
            if distancia >= distancia_minima:
                resultados.append(ruta)

    return resultados


import json
import math

from importacion import RUTA_ESTADO, cargar_estado


def mostrar_resultados(registros):
    """Imprime una lista de registros de forma legible."""

    if not registros:
        print("No se han encontrado coincidencias.")
        return

    print(f"\nCoincidencias: {len(registros)}")

    for registro in registros:
        print(json.dumps(
            registro,
            ensure_ascii=False,
            indent=2
        ))


def ejecutar_consultas():
    # Recuperamos el estado guardado en disco.
    try:
        estado = cargar_estado(RUTA_ESTADO)

    except (
        OSError,
        UnicodeError,
        json.JSONDecodeError,
        ValueError
    ) as error:
        print(f"No se puede cargar el estado: {error}")
        return

    rutas = estado["rutas"]
    planes = estado["planes"]

    print("Estado cargado correctamente.")
    print(f"Rutas disponibles: {len(rutas)}")
    print(f"Planes disponibles: {len(planes)}")

    while True:
        print("""
========= CONSULTAS =========
1. Buscar ruta por ID
2. Buscar plan por ID
3. Filtrar rutas por dificultad
4. Filtrar planes por estado
5. Buscar rutas por distancia mínima
0. Salir
""")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "0":
            print("Fin de las consultas.")
            break

        elif opcion == "1":
            identificador = input("ID de la ruta: ")
            resultado = buscar_por_id(
                rutas, "id_ruta", identificador
            )

            if resultado is None:
                mostrar_resultados([])
            else:
                mostrar_resultados([resultado])

        elif opcion == "2":
            identificador = input("ID del plan: ")
            resultado = buscar_por_id(
                planes, "id_plan", identificador
            )

            if resultado is None:
                mostrar_resultados([])
            else:
                mostrar_resultados([resultado])

        elif opcion == "3":
            dificultad = input(
                "Dificultad (fácil, moderada, difícil, muy difícil): "
            )

            resultados = filtrar_por_valor(
                rutas, "dificultad", dificultad
            )

            mostrar_resultados(resultados)

        elif opcion == "4":
            estado_plan = input(
                "Estado del plan (planificado o realizado): "
            )

            resultados = filtrar_por_valor(
                planes, "estado", estado_plan
            )

            mostrar_resultados(resultados)

        elif opcion == "5":
            texto = input(
                "Distancia mínima en km: "
            ).strip().replace(",", ".")

            try:
                distancia_minima = float(texto)

                if (
                    not math.isfinite(distancia_minima)
                    or distancia_minima < 0
                ):
                    raise ValueError(
                        "La distancia debe ser un número finito no negativo."
                    )

            except ValueError:
                print("Introduce una distancia válida, por ejemplo 10 o 12,5.")
                continue

            resultados = filtrar_rutas_por_distancia(
                rutas, distancia_minima
            )

            mostrar_resultados(resultados)

        else:
            print("Opción no válida. Elige una opción del menú.")


if __name__ == "__main__":
    ejecutar_consultas()
