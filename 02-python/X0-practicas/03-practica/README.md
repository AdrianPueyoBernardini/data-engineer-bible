# P2 - Base de datos PostgreSQL con Docker
 
Guía rápida para levantar, parar y gestionar el servidor PostgreSQL de la práctica P2.   
Lo primero, para activar las variables de entorno:

```bash
1 -> python -m venv .venv

2 -> .venv\Scripts\activate

3-> pip install -r requirements.txt
```


## Crear y lanzar el servidor (solo la primera vez)
 
```bash
docker run --name pg-p2 -e POSTGRES_PASSWORD=cambiame -e POSTGRES_DB=p2_rutas -p 5432:5432 -d postgres:16
```

| Parte | Qué hace |
|---|---|
| `--name pg-p2` | Nombre del contenedor (lo usarás en el resto de comandos) |
| `-e POSTGRES_PASSWORD=cambiame` | Contraseña del usuario `postgres` |
| `-e POSTGRES_DB=p2_rutas` | Crea la base de pruebas `p2_rutas` |
| `-p 5432:5432` | Expone el puerto de PostgreSQL en tu equipo |
| `-d` | Segundo plano |
| `postgres:16` | Imagen y versión |

---
 
## Comandos esenciales
 
| Acción | Comando |
|---|---|
| Ver contenedores en marcha | `docker ps` |
| Ver todos (también parados) | `docker ps -a` |
| **Parar** la base | `docker stop pg-p2` |
| **Arrancarla** de nuevo | `docker start pg-p2` |
| Reiniciar | `docker restart pg-p2` |
| Ver los logs | `docker logs pg-p2` |
| Seguir los logs en vivo | `docker logs -f pg-p2` (salir con `Ctrl+C`) |
 
Tras `docker stop` y `docker start`, **los datos se conservan**: siguen dentro del contenedor.
 
---