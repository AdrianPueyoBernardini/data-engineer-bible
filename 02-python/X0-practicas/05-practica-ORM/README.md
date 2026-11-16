# Práctica ORM: rutas y planes de viaje

Este proyecto demuestra una aplicación pequeña con SQLAlchemy y PostgreSQL para gestionar dos entidades:

- Ruta
- PlanViaje

La idea es practicar:

- mapeo ORM
- relación uno a muchos
- CRUD real
- transacciones con rollback
- SQL directo parametrizado
- validación con pruebas reales contra PostgreSQL

## Requisitos

- Python 3.12+
- Docker Desktop o Docker Engine
- Git
- PostgreSQL 18 (se ejecuta en contenedor local)

## Estructura del proyecto

- src/models.py: entidades y relación ORM
- src/db.py: conexión a la base
- src/orm_service.py: servicios con CRUD y consultas
- src/preparar_bd.py: crea la base y el esquema
- pruebas/: pruebas automatizadas
- config.ini.example: plantilla de configuración
- config.ini: configuración local que NO debe subirse a Git

## 1) Preparación rápida

Desde la raíz del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 2) Arrancar PostgreSQL

Si no tienes el contenedor creado, ejecuta:

```powershell
docker run --name pg-p2 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=postgres \
  -p 5433:5432 \
  -d postgres:18
```

> Si ya existe un contenedor con ese nombre, solo asegúrate de que escucha en el puerto 5433.

## 3) Configurar la conexión local

Copia la plantilla y modifica únicamente los valores que necesites:

```powershell
Copy-Item config.ini.example config.ini
```

Contenido esperado en config.ini:

```ini
[postgres]
host = localhost
port = 5433
dbname = p3_lab
user = postgres
password = cambia_esta_contraseña
```

Importante:

- config.ini se guarda localmente y queda ignorado por Git
- usa la contraseña real de tu PostgreSQL local o la que hayas definido para Docker
- la base debe terminar en _lab para que el script la cree de forma segura

## 4) Crear la base y el esquema

```powershell
python src/preparar_bd.py
```

Esto hace dos cosas:

1. crea la base p3_lab si no existe
2. crea el esquema del modelo ORM en PostgreSQL

## 5) Ejecutar pruebas

```powershell
pytest -q
```

O con el entorno virtual:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## 6) Qué se está validando

La práctica cubre cuatro bloques:

- H1: instalación, configuración y mapeo de tablas
- H2: CRUD y relación Ruta -> PlanViaje
- H3: transacciones con rollback y SQL parametrizado
- H4: pruebas y validación final

## 7) Regla de seguridad

Se ha dejado la configuración local fuera del repositorio:

- config.ini está ignorado por .gitignore
- no se guardan contraseñas ni credenciales reales en el proyecto
- el ejemplo de configuración queda en config.ini.example

## 8) Modelo de dominio

Entidades principales:

- Ruta: id, id_ruta, nombre, distancia_km, desnivel_m, valle, dificultad
- PlanViaje: id, id_plan, ruta_id, fecha_inicio, fecha_fin, estado

Relación:

- una Ruta puede tener muchos PlanViaje
- cada PlanViaje apunta a una Ruta
- la base impide borrar una Ruta si aún tiene planes asociados

## 9) Comandos útiles

```powershell
# Activar entorno
.\.venv\Scripts\Activate.ps1

# Verificar el entorno
python --version

# Reiniciar la base
python src/preparar_bd.py

# Reejecutar pruebas
pytest -q
```

## 10) Nota final

La práctica está diseñada para ejecutarse en local con un contenedor PostgreSQL y sin depender de secretos subidos al repositorio. Si alguien quiere replicarla en otra máquina, solo necesita:

- clonar el proyecto
- crear el entorno virtual
- arrancar Docker con PostgreSQL
- crear config.ini a partir de config.ini.example
- ejecutar src/preparar_bd.py y pytest
