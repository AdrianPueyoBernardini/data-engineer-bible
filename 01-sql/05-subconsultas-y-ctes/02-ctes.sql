--1.1 ¿Qué es una CTE?
--"Common Table Expression"
--Es básicamente ponerle un nombre temporal a una subconsulta, para usarla como si fuera una tabla normal en el resto de tu query. Se define con WITH.
WITH rutas_durillas AS (
	SELECT *
	FROM rutas
	WHERE distancia_km > (SELECT AVG(distancia_km) FROM rutas)
)
SELECT c.comarca_id,c.nombre, COUNT(*) AS total_rutas_exigentes
FROM rutas_durillas d
INNER JOIN comarcas c ON d.comarca_id = c.comarca_id
GROUP BY c.comarca_id, c.nombre
ORDER BY comarca_id ASC;

--Ejemplo 2: Tabla limpia temporal de nulos
WITH resenas_completas AS (
	SELECT * 
	FROM resenas
	WHERE comentario IS NOT NULL
)
SELECT * FROM resenas_completas;

--Ejemplo 3: Tabla limpia de nulos y con notas mayores a la media
WITH resenas_positivas AS (
	SELECT *
	FROM resenas
	WHERE comentario IS NOT NULL
	AND puntuacion > (SELECT AVG(puntuacion) FROM resenas)
)
SELECT * FROM resenas_positivas;


