# Chuleta: códigos de estado HTTP

| Rango | Significado | Códigos típicos | Qué quiere decir |
|-------|-------------|-----------------|------------------|
| **2xx** | Éxito | `200 OK` / `201 Created` | La petición fue recibida, entendida y aceptada correctamente. |
| **3xx** | Redirección | `301 Moved` / `304 Not Modified` | El cliente debe hacer acciones adicionales para completar la solicitud (ej: caché). |
| **4xx** | Error del cliente | `400 Bad Request` / `401 Unauthorized` / `404 Not Found` | Sintaxis errónea, faltan credenciales o el endpoint no existe. |
| **5xx** | Error del servidor | `500 Internal Server Error` / `503 Service Unavailable` | El servidor falló al procesar una petición válida (excepción de código o base de datos). |

## Casos que se confunden

| Código | Nombre | Cuándo |
|--------|--------|--------|
| `401` | Unauthorized | **No estás identificado** (faltan credenciales o son inválidas). |
| `403` | Forbidden | Estás autenticado, pero **no tienes el rol/permiso** para ese recurso. |
| `422` | Unprocessable Entity | Petición bien formada pero datos inválidos. **FastAPI lo devuelve solo** cuando falla la validación (ej: `/items/abc` con `item_id: int`). |

## En FastAPI

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/items", status_code=201)       # código de éxito personalizado
def create_item():
    return {"ok": True}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id != 1:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return {"item_id": item_id}
```