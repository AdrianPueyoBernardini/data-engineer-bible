# P2 · Acceso a PostgreSQL desde Python (con Docker)

Guía rápida para levantar el servidor PostgreSQL de la práctica P2, preparar la base y ejecutar las pruebas.
La explicación completa (esquema, reglas, pruebas y comparación de motores) está en [`DOCUMENTACION_P2.md`](DOCUMENTACION_P2.md).

Todos los comandos se ejecutan desde la carpeta `03-practica/`, salvo que se indique otra cosa.

---

## Requisitos

- Python 3.12
- Docker (Docker Desktop en Windows y Mac) **instalado y arrancado**

---

## 1. Entorno virtual y dependencias

El entorno virtual aísla las librerías de este proyecto. Se crea una sola vez y se activa en cada terminal nueva.

| Paso | Windows (PowerShell) | Windows (CMD) | Mac / Linux |
|---|---|---|---|
| Crear | `python -m venv .venv` | `python -m venv .venv` | `python3 -m venv .venv` |
| Activar | `.venv\Scripts\Activate.ps1` | `.venv\Scripts\activate.bat` | `source .venv/bin/activate` |
| Instalar dependencias | `pip install -r requirements.txt` | `pip install -r requirements.txt` | `pip install -r requirements.txt` |

Sabrás que está activo porque aparece `(.venv)` al principio de la línea de la terminal.

> En PowerShell, si bloquea la activación, ejecuta una vez: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

---

## 2. Crear y lanzar el servidor (solo la primera vez)

```bash
docker run --name pg-p2 -e POSTGRES_PASSWORD=12345 -e POSTGRES_DB=p2_rutas -p 5433:5432 -d postgres:16
```

| Parte | Qué hace |
|---|---|
| `--name pg-p2` | Nombre del contenedor (lo usarás en el resto de comandos) |
| `-e POSTGRES_PASSWORD=12345` | Contraseña del usuario `postgres` (de ejemplo; cámbiala si quieres) |
| `-e POSTGRES_DB=p2_rutas` | Crea la base de pruebas `p2_rutas` |
| `-p 5433:5432` | Puerto **5433 de tu equipo** → puerto 5432 dentro del contenedor |
| `-d` | Segundo plano |
| `postgres:16` | Imagen y versión |

> Se usa el puerto **5433** para no chocar con un PostgreSQL instalado en el equipo, que normalmente ocupa el 5432.
> Si no tienes ninguno, puedes usar `-p 5432:5432`, pero entonces debes poner `port = 5432` en `config.ini`.

Comprueba que está en marcha con `docker ps`: debe aparecer `pg-p2` con estado `Up`.

---

## 3. Configuración de la conexión

Copia el archivo de ejemplo y rellénalo con tus datos:

| Sistema | Comando |
|---|---|
| Windows | `copy config.example.ini config.ini` |
| Mac / Linux | `cp config.example.ini config.ini` |

Contenido de `config.ini` (debe coincidir con el `docker run`):

```ini
[postgres]
host = localhost
port = 5433
dbname = p2_rutas
user = postgres
password = 12345
```

`config.ini` contiene la contraseña y **está en `.gitignore`**: no se sube al repositorio. Lo que se comparte es `config.example.ini`, sin secretos.

---

## 4. Preparar la base

```bash
python src/preparar_bd.py
```

Aplica `sql/schema.sql` (tablas y restricciones) y `sql/procedimientos.sql` (procedimiento almacenado).

> **Atención:** este comando borra y recrea las tablas del proyecto (`ruta`, `plan_viaje`, `resumen_importacion`). Úsalo para empezar siempre desde un estado conocido. No toca otras bases.

Comprobación rápida de la conexión:

```bash
python src/probar_conexion.py
```

Debe imprimir `Resultado: (1,)`.

---

## 5. Ejecutar las pruebas

Orden recomendado, partiendo de la base recién preparada:

| Orden | Comando | Qué demuestra |
|---|---|---|
| 1 | `python src/probar_crud.py` | CRUD de rutas con parámetros (incluye texto con apóstrofo) |
| 2 | `python src/probar_planes.py` | CRUD de planes, consultas filtradas y con `JOIN` |
| 3 | `python src/probar_importador.py` | Importación sin duplicar: nuevos, duplicados, conflictos y rechazados |
| 4 | `python src/probar_transaccion.py` | Commit y rollback verificados desde otra conexión |
| 5 | `python src/probar_procedimiento.py` | Procedimiento almacenado, error y reversión |

> `probar_transaccion.py` parte de una base sin datos de ese lote. Si repites alguna prueba, ejecuta antes `python src/preparar_bd.py`.

---

## 6. Laboratorio con motor embebido (SQLite)

No necesita servidor ni instalación. Se ejecuta en **dos ejecuciones separadas** para comprobar que los datos persisten al reabrir:

```bash
python src/laboratorio_sqlite.py preparar
python src/laboratorio_sqlite.py reabrir
```

Crea el archivo `data/laboratorio.db`, que está ignorado por Git (`*.db`).

---

## 7. Comandos esenciales de Docker

Los comandos de `docker` son idénticos en Windows, Mac y Linux, y se pueden ejecutar desde cualquier carpeta.

| Acción | Comando |
|---|---|
| Ver contenedores en marcha | `docker ps` |
| Ver todos (también parados) | `docker ps -a` |
| **Parar** la base | `docker stop pg-p2` |
| **Arrancarla** de nuevo | `docker start pg-p2` |
| Reiniciar | `docker restart pg-p2` |
| Ver los logs | `docker logs pg-p2` |
| Seguir los logs en vivo | `docker logs -f pg-p2` (salir con `Ctrl+C`) |

Tras `docker stop` y `docker start`, **los datos se conservan**: siguen dentro del contenedor. Espera unos segundos tras arrancar antes de ejecutar los scripts.

> En Linux, si da "permission denied", añade tu usuario al grupo `docker` o antepón `sudo`.

---

## 8. Entrar a la base con psql

```bash
docker exec -it pg-p2 psql -U postgres -d p2_rutas
```

Dentro de `psql` no se usa el puerto 5433: estás dentro del contenedor.

| Comando | Qué hace |
|---|---|
| `\dt` | Lista las tablas |
| `\d ruta` | Describe la tabla `ruta` (columnas y restricciones) |
| `\sf renombrar_ruta` | Muestra la definición del procedimiento almacenado |
| `SELECT * FROM ruta;` | Consulta normal (acaba en `;`) |
| `\q` | Salir |

Una sola consulta sin entrar:

```bash
docker exec -it pg-p2 psql -U postgres -d p2_rutas -c "SELECT count(*) FROM ruta;"
```

---

## 9. Empezar desde cero

Solo las tablas (sin tocar el contenedor):

```bash
python src/preparar_bd.py
```

El contenedor entero, con todos sus datos:

```bash
docker stop pg-p2
docker rm pg-p2
```

Después se vuelve a ejecutar el `docker run` del apartado 2.

---

## 10. Problemas típicos

| Error | Causa y solución |
|---|---|
| `Cannot connect to the Docker daemon` / `error during connect` | Docker no está arrancado. Ábrelo y espera a que termine de iniciar |
| `port is already allocated` | Otro programa usa ese puerto. Cambia el primer número de `-p` y el `port` de `config.ini` |
| `container name "/pg-p2" is already in use` | Ya lo creaste. Usa `docker start pg-p2`, o bórralo con `docker rm pg-p2` |
| `password authentication failed` | La contraseña de `config.ini` no coincide con `POSTGRES_PASSWORD`, **o el puerto es de otro PostgreSQL** (un error en español suele indicar un PostgreSQL local). Revisa el puerto |
| `No encuentro config.ini` | Falta crear `config.ini` a partir de `config.example.ini` (apartado 3) |
| `ModuleNotFoundError: No module named 'psycopg'` | El entorno virtual no está activado o faltan las dependencias (apartado 1) |
| Un script no encuentra otro (`No module named 'db'`) | Ejecuta con `python src/nombre.py` desde la carpeta `03-practica/` |