--2.1 OPERADORES LOGICOS: AND // OR // IN
--El operador AND nos permite hacer condicione encadenadas 
SELECT nombre, distancia_km 
FROM rutas
WHERE distancia_km > 10
AND distancia_km < 15 ;

--2.2 El operador BETWEEN nos simplifica esto mucho
SELECT nombre, distancia_km 
FROM rutas
WHERE distancia_km BETWEEN 10 AND 15;

--2.3 Podemos usar el operador OR para añadir otras condiciones "o"
SELECT nombre, distancia_km 
FROM rutas
WHERE distancia_km = 14
OR distancia_km = 11;

--2.4 Podemos usar el operador IN para simplificar la sentencia
SELECT nombre, distancia_km
FROM rutas
WHERE distancia_km IN (11, 14);

--2.5 El operador NOT 
SELECT nombre, distancia_km , dificultad
FROM rutas
WHERE NOT dificultad = 'facil';

--2.6 El operador NOT + IN
SELECT nombre, distancia_km , dificultad
FROM rutas
WHERE dificultad NOT IN('facil', 'moderada');