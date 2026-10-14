from pathlib import Path
import os
import shutil
import tempfile
import filecmp


# Ruta raíz de la práctica
DIRECTORIO_PROYECTO = Path(__file__).resolve().parent.parent

DIRECTORIOS = {
    "entrada": DIRECTORIO_PROYECTO / "entrada",
    "salida": DIRECTORIO_PROYECTO / "salida",
    "trabajo": DIRECTORIO_PROYECTO / "trabajo",
    "pruebas": DIRECTORIO_PROYECTO / "pruebas",
    "src": DIRECTORIO_PROYECTO / "src",
}

DIRECTORIOS_IGNORADOS = {
    ".git",
    ".venv",
    "__pycache__"
}


def preparar_directorios():
    """Crea las carpetas necesarias si no existen."""

    for directorio in DIRECTORIOS.values():
        directorio.mkdir(
            parents=True,
            exist_ok=True
        )

    return DIRECTORIOS

def listar_archivos(directorio_raiz):
    """Devuelve archivos y tamaños, sin seguir enlaces simbólicos."""

    raiz = Path(directorio_raiz)

    if raiz.is_symlink():
        raise ValueError(
            "No se puede recorrer un enlace simbólico como raíz."
        )

    if not raiz.is_dir():
        raise FileNotFoundError(
            f"No existe el directorio: {raiz}"
        )

    archivos_encontrados = []

    for actual, directorios, archivos in os.walk(
        raiz,
        topdown=True,
        followlinks=False
    ):
        carpeta_actual = Path(actual)

        # Excluimos directorios innecesarios y enlaces simbólicos.
        directorios[:] = [
            nombre
            for nombre in directorios
            if nombre not in DIRECTORIOS_IGNORADOS
            and not (carpeta_actual / nombre).is_symlink()
        ]

        for nombre in archivos:
            archivo = carpeta_actual / nombre

            if archivo.is_symlink():
                continue

            if not archivo.is_file():
                continue

            archivos_encontrados.append({
                "nombre": str(archivo.relative_to(raiz)),
                "tamano_bytes": archivo.stat().st_size
            })

    return sorted(
        archivos_encontrados,
        key=lambda archivo: archivo["nombre"].casefold()
    )

def demostrar_operaciones():
    """Copia, mueve y elimina una copia sin tocar el original."""

    preparar_directorios()

    original = DIRECTORIOS["entrada"] / "rutas.csv"

    if original.is_symlink() or not original.is_file():
        raise FileNotFoundError(
            f"No se encuentra un CSV original válido: {original}"
        )

    tamano_original = original.stat().st_size

    # Carpeta temporal aislada dentro de trabajo/
    with tempfile.TemporaryDirectory(
        prefix="demostracion_",
        dir=DIRECTORIOS["trabajo"]
    ) as directorio_temporal:

        carpeta_temporal = Path(directorio_temporal)

        copia = carpeta_temporal / "copia_rutas.csv"
        archivo_movido = carpeta_temporal / "rutas_movidas.csv"

        # 1. COPIAR
        shutil.copy2(original, copia)

        if not filecmp.cmp(original, copia, shallow=False):
            raise OSError(
                "La copia no coincide con el archivo original."
            )

        print("COPIA: correcta. El contenido coincide.")

        # 2. MOVER la copia dentro de la carpeta temporal
        shutil.move(copia, archivo_movido)

        if copia.exists() or not archivo_movido.is_file():
            raise OSError("No se ha podido verificar el movimiento.")

        print("MOVIMIENTO: correcto.")

        # 3. ELIMINAR solo la copia movida
        archivo_movido.unlink()

        if archivo_movido.exists():
            raise OSError("El archivo temporal no se ha eliminado.")

        print("ELIMINACIÓN: correcta.")

    # 4. Comprobar que el original sigue existiendo y conserva su tamaño.
    if (
        original.is_symlink()
        or not original.is_file()
        or original.stat().st_size != tamano_original
    ):
        raise OSError(
            "El archivo original ha desaparecido o ha cambiado de tamaño."
        )

    print("ORIGINAL: conservado correctamente.")

def main():
    try:
        print("=== PREPARAR DIRECTORIOS ===")

        directorios = preparar_directorios()

        for nombre, ruta in directorios.items():
            print(f"{nombre}: {ruta}")

        print("\n=== LISTADO DE ARCHIVOS ===")

        archivos = listar_archivos(DIRECTORIO_PROYECTO)

        for archivo in archivos:
            print(
                f"{archivo['nombre']} "
                f"- {archivo['tamano_bytes']} bytes"
            )

        print("\n=== OPERACIONES CON ARCHIVOS ===")

        demostrar_operaciones()

    except (OSError, ValueError) as error:
        print(f"ERROR: {error}")


if __name__ == "__main__":
    main()