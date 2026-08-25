--4.1 LIMIT básico
--Tal y como hemos visto antes, limit es muy útil para no hacer carga de tantos ficheros simultaneos
SELECT resena_id, comentario
FROM resenas
LIMIT 3;

--4.2 OFFSET: filas a saltar hasta darnos la sentencia, (se puede utilizar sin el limit)
SELECT resena_id, comentario
FROM resenas
LIMIT 3 OFFSET 3;