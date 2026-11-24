# Acceso a datos 

## 🗂️ ¿Qué es un motor de base de datos?
Es el software responsable de almacenar, recuperar y modificar los datos.

## 🗂️ Tipos de motores de BBDD
>1. Motor embebido  
>2. Servidor de BBDD independiente  

### 1. Motor embebido
El motor embebido funciona dentro de la propia aplicación, en local, no requiere de ningún servidor externo para ser gestionado.


| Ventajas | Inconvenientes |
| --- | --- |
| Sin servidor externo | Lecturas limitadas |
| Ligero y admite SQL | Peor escalabilidad (es local) |
| Todo en un archivo | Más inseguro, local = expuesto |

### 2. Servidor independiente
El motor aquí es un servicio independiente, un ejemplo sería PostgreSQL
Requiere (además de un puerto, como en postgresql el 5432):   
```<python>
    host="localhost",   
    dbname="postgres",     
    user="postgres",     
    password="postgres" 
```
