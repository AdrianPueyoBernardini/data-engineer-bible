--1. SELECT básico
SELECT nombre FROM ibones;

--1.1 SELECT con un límite de consultas, genial para produccion
SELECT nombre FROM ibones LIMIT 5;

--1.2 SELECT + AS para visualizar el campo de forma personalizada
SELECT nombre, altitud_m as "altitud" FROM ibones;

--1.4 SELECT + ORDER BY: Ordenación de mayor a menor
SELECT nombre, altitud_m
FROM ibones
ORDER BY altitud_m asc
LIMIT 5; 