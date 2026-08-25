--2.1 WHERE básico
SELECT nombre, distancia_km
FROM rutas
WHERE distancia_km > 10;

SELECT nombre, distancia_km AS "km", desnivel_m
FROM rutas
WHERE circular = true;

--2.2 WHERE + OR: multi condicion "o"
SELECT nombre, distancia_km, desnivel_m, dificultad
FROM rutas
WHERE dificultad = 'dificil'
OR dificultad = 'muy_dificil';

--2.3 WHERE + IN: Multicondición "o" más limpia
SELECT nombre, dificultad 
FROM rutas
WHERE dificultad IN ('dificil', 'muy_dificil');

--2.4 WHERE + AND: multi condicion "y"
SELECT nombre, distancia_km, dificultad
FROM rutas
WHERE distancia_km > 15
AND dificultad = 'muy_dificil';