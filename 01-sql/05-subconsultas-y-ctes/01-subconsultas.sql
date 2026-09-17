--1.1 ¿Qué es una subconsulta?
--Son consultas anidadas con varios SELECTS
--Aquí va una comparación para ver ejemplos de uso
SELECT *
FROM rutas
WHERE distancia_km > (SELECT AVG(distancia_km) FROM rutas);

--VS

SELECT AVG(distancia_km) FROM rutas; --Esto da 11.175

SELECT * 
FROM rutas
WHERE distancia_km > 11.175
LIMIT 10;

--Ejemplo 2

SELECT *
FROM rutas
WHERE desnivel_m > (SELECT AVG(desnivel_m) FROM rutas);

-- SELECT * FROM rutas WHERE desnivel_m > AVG(desnivel_m); --Esto jamás ejecutaría ya que la función de agregación ha de ir antes.




