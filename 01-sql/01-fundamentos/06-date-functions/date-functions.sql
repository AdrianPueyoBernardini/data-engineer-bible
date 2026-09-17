--6.1 DATE FUNCTIONS:
SELECT resena_id,
fecha_resena,							   --Nuestro valor base
fecha_resena::DATE AS date,				   --Nos ofrece la fecha exclusivamente
fecha_resena::TIMESTAMP AS timestamp,	   --Fecha de la reseña (asume que es 0 ya que están hardcodeadas)
fecha_resena::TIMESTAMPTZ AS timestamptz   --Fecha + mi hora horaria
FROM resenas;

--6.2 EXTRACT: Podemos extraer una parte de la fecha 
SELECT resena_id,
EXTRACT(YEAR FROM fecha_resena) AS ano,
EXTRACT(MONTH FROM fecha_resena) AS mes,
EXTRACT(DAY FROM fecha_resena) AS dia
FROM resenas;

--6.3 EXTRACT + GROUP BY ¿Cuantas reseás tenemos por año?
SELECT EXTRACT(YEAR FROM fecha_resena) AS ano,
COUNT(EXTRACT(YEAR FROM fecha_resena))
FROM resenas
WHERE fecha_resena IS NOT NULL
GROUP BY EXTRACT(YEAR FROM fecha_resena);

-- Y por mes?
SELECT EXTRACT(MONTH FROM fecha_resena) AS mes,
COUNT(EXTRACT(MONTH FROM fecha_resena))
FROM resenas
WHERE fecha_resena IS NOT NULL 
GROUP BY EXTRACT(MONTH FROM fecha_resena)
ORDER BY EXTRACT(MONTH FROM fecha_resena) ASC;