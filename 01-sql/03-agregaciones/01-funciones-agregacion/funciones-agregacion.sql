--1.1 Funciones agregacion: COUNT, SUM, AVG, MIN, MAX
--COUNT: Permite contar el total de filas.
--IMPORTATE: (*) cuenta cada fila, por el contrario, COUNT(comentario) cuenta solamenta valores NO NULOS
SELECT COUNT(comentario) --Esto da 37
FROM resenas;

SELECT COUNT(*) --Esto da 52(cuenta también los nulos)
FROM resenas;

--1.2 COUNT + DISTINCT: Contamos los valores DIFERENTES, en este caso su hubiera varias reseñas de un mismo autor solo contaría x1
SELECT ruta_id, COUNT(DISTINCT autor)
FROM resenas
GROUP BY ruta_id
ORDER BY ruta_id ASC;

--1.3 SUM
--Sumatorio total de un campo
SELECT SUM(desnivel_m)
FROM rutas;

--1.4 AVG
--Podemos sacar una media de cada una de las rutas (agrupando por id)
SELECT ruta_id, AVG(puntuacion) AS "media de puntuación"
FROM resenas
GROUP BY ruta_id
ORDER BY ruta_id ASC;

--1.4 AVG + ROUND
--También podemos redondear con ROUND(VALOR, DECIMALES)
SELECT ruta_id, ROUND(AVG(puntuacion),1) AS "media de puntuación"
FROM resenas
GROUP BY ruta_id
ORDER BY ruta_id ASC;

--1.6 MIN/MAX
--Podemos a su vez sacar el máximo y mínimo
SELECT ruta_id, MAX(puntuacion) AS "maxima nota", MIN(puntuacion) AS "minima nota"
FROM resenas
GROUP BY ruta_id
ORDER BY ruta_id ASC;