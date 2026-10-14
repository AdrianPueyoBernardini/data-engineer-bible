
import sys
import csv
import json
import tempfile
import unittest

from pathlib import Path
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch


# Añadir src al camino de búsqueda de módulos.
RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "src"))

import importacion

from lectura import leer_csv, leer_json, RUTA_CSV, RUTA_JSON
from validacion import validar_ruta, validar_plan

from importacion import clasificar_lote

from consultas import (
    buscar_por_id,
    filtrar_por_valor,
    filtrar_rutas_por_distancia
)


# ---------- DATOS AUXILIARES ----------

def fila_ruta(
    id_ruta="R01",
    ruta="Ruta de prueba",
    distancia="12,5",
    desnivel="300",
    valle="Valle de prueba",
    dificultad="moderada"
):
    return {
        "id_ruta": id_ruta,
        "ruta": ruta,
        "distancia_km": distancia,
        "desnivel_m": desnivel,
        "valle": valle,
        "dificultad": dificultad
    }


def fila_plan(
    id_plan="P01",
    id_ruta="R01",
    inicio="2026-10-18",
    fin="2026-10-19",
    estado="planificado"
):
    return {
        "id_plan": id_plan,
        "id_ruta": id_ruta,
        "fecha_inicio": inicio,
        "fecha_fin": fin,
        "estado": estado
    }


def preparar_salidas(directorio, estado_texto=None):
    salida = directorio / "salida"
    salida.mkdir(parents=True, exist_ok=True)

    ruta_estado = salida / "estado.json"
    ruta_informe = salida / "informe.json"

    if estado_texto is None:
        estado_texto = '{"rutas": [], "planes": []}'

    ruta_estado.write_text(estado_texto, encoding="utf-8")
    ruta_informe.write_text(
        '{"anterior": true}',
        encoding="utf-8"
    )

    return ruta_estado, ruta_informe


CSV_VALIDO = (
    "id_ruta,ruta,distancia_km,desnivel_m,valle,dificultad\n"
    'R01,"Ruta de prueba","12,5",300,"Valle de prueba",moderada\n'
)


# ---------- PRUEBAS ----------

class PruebasPractica(unittest.TestCase):

    def test_dataset_tiene_minimos(self):
        rutas_validas = []

        for fila in leer_csv(RUTA_CSV):
            registro, motivo = validar_ruta(fila)

            if motivo is None:
                rutas_validas.append(registro)

        ids_rutas = {
            ruta["id_ruta"] for ruta in rutas_validas
        }

        planes_validos = []

        for fila in leer_json(RUTA_JSON):
            registro, motivo = validar_plan(fila, ids_rutas)

            if motivo is None:
                planes_validos.append(registro)

        self.assertGreaterEqual(len(rutas_validas), 5)
        self.assertGreaterEqual(len(planes_validos), 8)

    def test_desnivel_desconocido(self):
        registro, motivo = validar_ruta(
            fila_ruta(desnivel="—")
        )

        self.assertIsNone(motivo)
        self.assertIsNone(registro["desnivel_m"])

    def test_distancia_invalida(self):
        registro, motivo = validar_ruta(
            fila_ruta(distancia="muchas")
        )

        self.assertIsNone(registro)
        self.assertIn("TIPO_INCORRECTO", motivo)

        registro, motivo = validar_ruta(
            fila_ruta(distancia="-2")
        )

        self.assertIsNone(registro)
        self.assertIn("RANGO", motivo)

    def test_fechas_invalidas_o_incoherentes(self):
        registro, motivo = validar_plan(
            fila_plan(inicio="2026-02-30"),
            {"R01"}
        )

        self.assertIsNone(registro)
        self.assertIn("FECHA_INVALIDA", motivo)

        registro, motivo = validar_plan(
            fila_plan(
                inicio="2026-11-22",
                fin="2026-11-19"
            ),
            {"R01"}
        )

        self.assertIsNone(registro)
        self.assertIn("FECHAS_INCOHERENTES", motivo)

    def test_referencia_inexistente(self):
        registro, motivo = validar_plan(
            fila_plan(id_ruta="R99"),
            {"R01"}
        )

        self.assertIsNone(registro)
        self.assertIn("REFERENCIA_INEXISTENTE", motivo)

    def test_clasificacion_de_registros(self):
        original, motivo = validar_ruta(
            fila_ruta(
                id_ruta="R99",
                distancia="1,5",
                desnivel="100",
                dificultad="fácil"
            )
        )
        self.assertIsNone(motivo)

        filas = [
            # Duplicado
            fila_ruta(
                id_ruta="R99",
                distancia="1,5",
                desnivel="100",
                dificultad="fácil"
            ),

            # Conflicto: misma identidad, contenido distinto
            fila_ruta(
                id_ruta="R99",
                distancia="2",
                desnivel="100",
                dificultad="fácil"
            ),

            # Nuevo
            fila_ruta(
                id_ruta="R100",
                distancia="3",
                desnivel="200"
            ),

            # Rechazado
            fila_ruta(
                id_ruta="R101",
                distancia="muchas"
            )
        ]

        resultado = clasificar_lote(
            filas=filas,
            registros_anteriores=[original],
            campo_id="id_ruta",
            archivo="prueba.csv",
            validador=validar_ruta
        )

        self.assertEqual(
            resultado["resumen"],
            {
                "procesados": 4,
                "nuevos": 1,
                "duplicados": 1,
                "conflictos": 1,
                "rechazados": 1
            }
        )

        rutas_estado = {
            ruta["id_ruta"]: ruta
            for ruta in resultado["estado"]
        }

        # El conflicto no reemplaza el registro anterior.
        self.assertEqual(
            rutas_estado["R99"]["distancia_km"],
            1.5
        )

        self.assertIn("R100", rutas_estado)
        self.assertNotIn("R101", rutas_estado)

    def test_csv_con_tildes_comas_y_lineas_vacias(self):
        with tempfile.TemporaryDirectory() as temporal:
            archivo = Path(temporal) / "prueba.csv"

            with archivo.open(
                "w",
                encoding="utf-8",
                newline=""
            ) as salida:
                salida.write(
                    "id_ruta,ruta,distancia_km,desnivel_m,"
                    "valle,dificultad\n"
                    '\n'
                    'R01,"Pradera, río","17,5",300,'
                    '"Valle de Ordesa",difícil\n'
                )

            filas = list(leer_csv(archivo))

        self.assertEqual(len(filas), 1)
        self.assertEqual(filas[0]["ruta"], "Pradera, río")

        registro, motivo = validar_ruta(filas[0])

        self.assertIsNone(motivo)
        self.assertEqual(registro["distancia_km"], 17.5)
        self.assertEqual(registro["valle"], "Valle de Ordesa")

    def test_funciones_de_consulta(self):
        ruta_1, _ = validar_ruta(
            fila_ruta(
                id_ruta="R01",
                distancia="12",
                dificultad="fácil"
            )
        )

        ruta_2, _ = validar_ruta(
            fila_ruta(
                id_ruta="R02",
                distancia="25",
                dificultad="difícil"
            )
        )

        rutas = [ruta_1, ruta_2]

        resultado = buscar_por_id(
            rutas, "id_ruta", "R01"
        )
        self.assertEqual(resultado["id_ruta"], "R01")

        filtradas = filtrar_por_valor(
            rutas, "dificultad", "DIFÍCIL"
        )
        self.assertEqual(len(filtradas), 1)
        self.assertEqual(filtradas[0]["id_ruta"], "R02")

        largas = filtrar_rutas_por_distancia(rutas, 20)
        self.assertEqual(len(largas), 1)
        self.assertEqual(largas[0]["id_ruta"], "R02")

        inexistente = buscar_por_id(
            rutas, "id_ruta", "R99"
        )
        self.assertIsNone(inexistente)

    def test_json_malformado_no_modifica_salidas(self):
        with tempfile.TemporaryDirectory() as temporal:
            base = Path(temporal)

            estado, informe = preparar_salidas(base)

            csv_path = base / "rutas.csv"
            json_path = base / "planes.json"

            csv_path.write_text(CSV_VALIDO, encoding="utf-8")
            json_path.write_text(
                '{"registro": ',
                encoding="utf-8"
            )

            estado_anterior = estado.read_bytes()
            informe_anterior = informe.read_bytes()

            with (
                patch.object(importacion, "RUTA_ESTADO", estado),
                patch.object(importacion, "RUTA_INFORME", informe),
                patch.object(importacion, "RUTA_CSV", csv_path),
                patch.object(importacion, "RUTA_JSON", json_path)
            ):
                with redirect_stdout(StringIO()):
                    importacion.ejecutar_importacion()

            self.assertEqual(estado.read_bytes(), estado_anterior)
            self.assertEqual(informe.read_bytes(), informe_anterior)

    def test_entrada_inexistente_no_modifica_salidas(self):
        with tempfile.TemporaryDirectory() as temporal:
            base = Path(temporal)

            estado, informe = preparar_salidas(base)

            csv_path = base / "no_existe.csv"
            json_path = base / "planes.json"
            json_path.write_text("[]", encoding="utf-8")

            estado_anterior = estado.read_bytes()
            informe_anterior = informe.read_bytes()

            with (
                patch.object(importacion, "RUTA_ESTADO", estado),
                patch.object(importacion, "RUTA_INFORME", informe),
                patch.object(importacion, "RUTA_CSV", csv_path),
                patch.object(importacion, "RUTA_JSON", json_path)
            ):
                with redirect_stdout(StringIO()):
                    importacion.ejecutar_importacion()

            self.assertEqual(estado.read_bytes(), estado_anterior)
            self.assertEqual(informe.read_bytes(), informe_anterior)

    def test_estado_corrupto_no_se_sustituye_por_vacio(self):
        with tempfile.TemporaryDirectory() as temporal:
            base = Path(temporal)

            estado, informe = preparar_salidas(
                base,
                estado_texto='{"rutas":'
            )

            csv_path = base / "rutas.csv"
            json_path = base / "planes.json"

            csv_path.write_text(CSV_VALIDO, encoding="utf-8")
            json_path.write_text("[]", encoding="utf-8")

            estado_anterior = estado.read_bytes()
            informe_anterior = informe.read_bytes()

            with (
                patch.object(importacion, "RUTA_ESTADO", estado),
                patch.object(importacion, "RUTA_INFORME", informe),
                patch.object(importacion, "RUTA_CSV", csv_path),
                patch.object(importacion, "RUTA_JSON", json_path)
            ):
                with redirect_stdout(StringIO()):
                    importacion.ejecutar_importacion()

            self.assertEqual(estado.read_bytes(), estado_anterior)
            self.assertEqual(informe.read_bytes(), informe_anterior)

    def test_json_supera_limite_de_tamano(self):
        with tempfile.TemporaryDirectory() as temporal:
            archivo = Path(temporal) / "grande.json"
            archivo.write_text(
                '{"dato": "este contenido excede el límite"}',
                encoding="utf-8"
            )

            with self.assertRaises(ValueError):
                leer_json(archivo, max_bytes=10)


if __name__ == "__main__":
    unittest.main()
