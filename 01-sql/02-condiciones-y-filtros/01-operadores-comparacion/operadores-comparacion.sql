-- 1.1 OPERADORES DE COMPARACIÓN: =, <>, >, <, >=, <=
-- Operador Mayor/menor que > <
SELECT ibon_id, nombre, altitud_m 
FROM ibones
WHERE altitud_m > 2000;

-- 1.2 Operador = que
SELECT ibon_id, nombre, altitud_m 
FROM ibones
WHERE altitud_m = 2500;