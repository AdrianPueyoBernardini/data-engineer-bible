--4.1 CASE
-- Podemos crear una columna que según la condición tenga un valor u otro
SELECT nombre, distancia_km, desnivel_m,
	CASE
		WHEN desnivel_m < 500 THEN 'Facil'
		WHEN desnivel_m BETWEEN 500 AND 1000 THEN 'Moderado'
		WHEN desnivel_m IS NULL THEN 'Sin datos...'
		ELSE 'Dificil'
	END AS Dificultad
FROM rutas
ORDER BY desnivel_m DESC;

--Muy util para filtrar
SELECT autor, puntuacion, comentario,
	CASE
		WHEN puntuacion <= 3 THEN 'baja puntuacion'
		WHEN puntuacion = 4 THEN 'media puntuacion'
		ELSE 'alta puntuacion'
	END AS Puntuacion
FROM resenas;