--3.1 LIKE: %dobleporcentaje%
-- Con LIKE podemos filtrar por nombres
--Si ponemos un % delante y otro detrás detecta de informa indifernte todo lo que esté delante y detrás de la selección
SELECT * 
FROM ibones
WHERE nombre LIKE '%Pied%';

--3.2 % Simple -> ¡cuidado! es case sensitive
--Filtramos por todo lo que empiece por Ibón
SELECT * 
FROM ibones
WHERE nombre LIKE 'Ibón%';

--3.3 NOT LIKE
SELECT * 
FROM ibones
WHERE nombre NOT LIKE '%Bachimaña%';