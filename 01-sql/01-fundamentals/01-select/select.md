##  SELECT

> **1. SELECT**     
SELECT nombre FROM ibones; 

> **2. SELECT + LIMIT: Límites de consultas**  
SELECT nombre FROM ibones LIMIT 5;  

> **3. SELECT + AS: Cambio de nombre de los campos**  
SELECT nombre, altitud_m as "altitud" FROM ibones;  

> **4. SELECT + ORDER BY: Ordenación de mayor a menor**  
SELECT nombre, altitud_m  
FROM ibones  
ORDER BY altitud_m asc  
LIMIT 5;  
