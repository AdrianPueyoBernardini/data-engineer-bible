--1.1 INNER JOIN
--Con INNER JOIN encontramos las coincidencias de dos tablas diferentes enlazadas entre si.
--Tienen que pertenecer a ambas tablas
SELECT r.ruta_id, r.autor, r.comentario, ru.nombre
FROM resenas r 
INNER JOIN rutas ru
ON r.ruta_id = ru.ruta_id
ORDER BY ruta_id ASC;





