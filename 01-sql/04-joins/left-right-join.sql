--2.1 LEFT JOIN
--Con LEFT JOIN encontramos las coincidencias de dos tablas diferentes enlazadas entre si.
--Mostrará TODAS las reseñas que tengan asignada o no ruta, y las que no tengan ruta aparecerán como NULL
SELECT r.ruta_id, r.autor, r.comentario, ru.nombre
FROM resenas r 
LEFT JOIN rutas ru
ON r.ruta_id = ru.ruta_id
ORDER BY ruta_id ASC;
