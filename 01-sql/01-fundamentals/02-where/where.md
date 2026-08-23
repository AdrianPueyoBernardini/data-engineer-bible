##  WHERE

> **1. WHERE**     
SELECT nombre, distancia_km  
FROM rutas  
WHERE distancia_km > 10;  

>SELECT nombre, distancia_km AS "km", desnivel_m  
FROM rutas  
WHERE circular = true; 

> **2. WHERE + OR: multi condicion "o"**  
SELECT nombre, distancia_km, desnivel_m, dificultad  
FROM rutas  
WHERE dificultad = 'dificil'  
OR dificultad = 'muy_dificil';    

> **3. WHERE + OR: multi condicion "y"**  
SELECT nombre, distancia_km, dificultad  
FROM rutas  
WHERE distancia_km > 15  
AND dificultad = 'muy_dificil';  