
# P1 — Gestor de rutas y planes de senderismo

## 1. Objetivo

Aplicación Python para importar, validar, normalizar y gestionar
datos sobre rutas de senderismo y planes de excursión.

El programa lee datos CSV y JSON, detecta registros nuevos,
duplicados, conflictos y rechazados, guarda un estado persistente
y genera un informe de la última importación.

## 2. Entidades y reglas de datos

### Rutas (A)

Archivo de entrada: `entrada/rutas.csv`

| Campo | Tipo normalizado | Regla |
|---|---|---|
| id_ruta | str | Identificador con formato R seguido de al menos dos dígitos |
| ruta | str | Obligatorio |
| distancia_km | float | Número finito mayor que cero |
| desnivel_m | int o None | Entero no negativo; — representa un valor desconocido |
| valle | str | Obligatorio |
| dificultad | str | fácil, moderada, difícil o muy difícil |

### Planes (B)

Archivo de entrada: `entrada/planes.json`

| Campo | Tipo | Regla |
|---|---|---|
| id_plan | str | Identificador con formato P seguido de al menos dos dígitos |
| id_ruta | str | Debe corresponder a una ruta válida |
| fecha_inicio | str | Fecha real en formato AAAA-MM-DD |
| fecha_fin | str | Fecha real igual o posterior a fecha_inicio |
| estado | str | planificado o realizado |

### Identidad y campos desconocidos

La identidad de las rutas es `id_ruta` y la de los planes es `id_plan`.

Las columnas o propiedades adicionales no se incorporan al modelo
normalizado. Las columnas CSV adicionales declaradas en la cabecera
se ignoran; una fila con más valores que la cabecera se considera
un error de lectura.

Los espacios exteriores se eliminan. El resto del texto se conserva
sin cambiar arbitrariamente las mayúsculas ni las tildes.

## 3. Estructura del proyecto

    entrada/
        rutas.csv
        planes.json
    salida/
        estado.json
        informe.json
    trabajo/
    pruebas/
    src/
        lectura.py
        validacion.py
        importacion.py
        consultas.py
        gestion_archivos.py

## 4. Requisitos

- Python 3.10 o superior.
- No requiere paquetes externos; utiliza la biblioteca estándar.

## 5. Ejecución

Ejecutar los comandos desde la raíz de `02-practica`.

### Importar datos

    python src/importacion.py

### Consultar el estado guardado

    python src/consultas.py

### Probar la gestión de archivos

    python src/gestion_archivos.py

### Ejecutar pruebas automatizadas

    python -m unittest discover -s pruebas -p "test_*.py" -v

## 6. Lectura y persistencia

El CSV se procesa secuencialmente mediante un generador.
Se utiliza UTF-8, coma como separador y la primera fila como cabecera.

El JSON se lee completo con un tamaño máximo configurable de 1 MB.

El programa no modifica las entradas originales.

`salida/estado.json` conserva las rutas y planes normalizados
aceptados en esta ejecución o en anteriores.

`salida/informe.json` contiene los contadores de rutas y planes,
así como las incidencias de la última importación.

El valor Python None se representa como null en JSON.

## 7. Clasificación

- Nuevo: identificador desconocido y registro válido.
- Duplicado: misma identidad y mismo contenido normalizado.
- Conflicto: misma identidad, pero contenido válido diferente.
- Rechazado: registro que incumple el contrato o una referencia.

Un registro inválido no reserva una identidad.
Los conflictos no reemplazan el contenido anterior.
Las entidades que no aparecen en una entrada no se eliminan
del estado persistente.

## 8. Pruebas y resultados

| Caso | Resultado esperado | Resultado obtenido |
|---|---|---|
| Primera importación válida | Incorporar los registros nuevos | Completar tras ejecutar |
| Campo obligatorio vacío | Rechazar e indicar el campo | Completar tras ejecutar |
| Tipo o rango inválido | Rechazar e indicar el motivo | Completar tras ejecutar |
| Referencia inexistente | Rechazar el plan | Completar tras ejecutar |
| Repetir una importación | No duplicar registros guardados | Completar tras ejecutar |
| Identidad con contenido diferente | Conflicto y conservación del anterior | Completar tras ejecutar |
| CSV con tildes, comas y líneas vacías | Interpretar correctamente los campos | Completar tras ejecutar |
| JSON ilegible o entrada inexistente | Informar del error y conservar las salidas | Completar tras ejecutar |
| Estado anterior corrupto | Informar del error sin sustituirlo por uno vacío | Completar tras ejecutar |
| Reiniciar y consultar | Recuperar los datos desde disco | Completar tras ejecutar |
| Copiar, mover y eliminar una copia | Completar las operaciones y conservar el original | Completar tras ejecutar |

Actualizar la columna "Resultado obtenido" con los resultados
observados durante las pruebas reales.

## 9. Limitaciones conocidas

Las dos salidas JSON se escriben mediante operaciones separadas.
No se garantiza una actualización atómica conjunta si ocurre un
fallo durante la escritura.

La publicación por versiones, la conversión XML y el acceso a
archivos binarios son ampliaciones opcionales y no forman parte
del alcance mínimo implementado.
