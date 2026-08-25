--5.1 NOT NULL
--Podemos filtrar los nulos para evitarlos
SELECT  autor, comentario, fecha_resena AS "fecha", puntuacion
FROM resenas
WHERE comentario IS NOT NULL;

--5.2 IS NULL
--Nos puede por el contrario interesar modificar los campos nulos, por ello podemos hacer también lo contrarío
SELECT  autor, comentario, fecha_resena AS "fecha", puntuacion
FROM resenas
WHERE comentario IS NULL;

--5.3 COALESCE
--Una sentencia muy útil, reemplaza los valores nulos por lo que le digamos
--si no renombramos la columna, pondrá "coalesce", por lo que es recomendado acompañarla de AS
SELECT autor, COALESCE(comentario, 'Sin comentarios del usuario...') AS "comentario"
FROM resenas;

--5.4 NULLIF
--Podemos querer lo contrario, convertir a nulos
SELECT autor, NULLIF(puntuacion, 3) AS "puntuacion", comentario
FROM resenas;