-- ============================================================
-- BASE DE DATOS DE PRÁCTICA: EXCURSIONES E IBONES DEL PIRINEO
-- Autor: Adrián | Uso: práctica SQL en PostgreSQL
-- v2: más registros reales + valores NULL para practicar
--     (COALESCE, IS NULL / IS NOT NULL, agregaciones con NULL, LEFT JOIN, etc.)
-- ============================================================

-- Limpieza previa (por si se ejecuta varias veces)
DROP TABLE IF EXISTS resenas CASCADE;
DROP TABLE IF EXISTS ruta_ibon CASCADE;
DROP TABLE IF EXISTS rutas CASCADE;
DROP TABLE IF EXISTS ibones CASCADE;
DROP TABLE IF EXISTS comarcas CASCADE;
DROP TYPE IF EXISTS nivel_dificultad CASCADE;

-- ============================================================
-- TIPOS PERSONALIZADOS
-- ============================================================

CREATE TYPE nivel_dificultad AS ENUM ('facil', 'moderada', 'dificil', 'muy_dificil');

-- ============================================================
-- TABLA: comarcas
-- ============================================================

CREATE TABLE comarcas (
    comarca_id      SERIAL PRIMARY KEY,
    nombre          VARCHAR(50) NOT NULL UNIQUE,
    provincia       VARCHAR(50) NOT NULL DEFAULT 'Huesca',
    descripcion     TEXT            -- nullable: aún no todas las comarcas están documentadas
);

INSERT INTO comarcas (nombre, provincia, descripcion) VALUES
('Valle de Tena',   'Huesca', 'Valle pirenaico famoso por Sallent de Gállego y Panticosa'),
('Jacetania',       'Huesca', 'Comarca del Pirineo occidental aragonés, capital Jaca'),
('Sobrarbe',        'Huesca', 'Comarca que alberga el Parque Nacional de Ordesa y Monte Perdido'),
('Sierra de Guara', 'Huesca', 'Conocida por barrancos y cañones, sur del Pirineo'),
('Alto Gállego',    'Huesca', 'Comarca pirenaica con capital en Sabiñánigo, incluye Panticosa y Formigal'),
('Ribagorza',       'Huesca', NULL);   -- descripción pendiente de redactar -> NULL real

-- ============================================================
-- TABLA: ibones
-- ============================================================

CREATE TABLE ibones (
    ibon_id         SERIAL PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    comarca_id      INTEGER NOT NULL REFERENCES comarcas(comarca_id),
    altitud_m       INTEGER CHECK (altitud_m > 0),
    superficie_ha   NUMERIC(6,2),   -- nullable: no siempre hay dato catastral/medido
    profundidad_m   NUMERIC(5,2)    -- nullable: muchos ibones no tienen batimetría publicada
);

INSERT INTO ibones (nombre, comarca_id, altitud_m, superficie_ha, profundidad_m) VALUES
-- Valle de Tena / Alto Gállego
('Ibón de Piedrafita',        1, 1635, 12.50, 12.00),
('Ibón de Bachimaña',         1, 2237,  6.80, 30.00),
('Ibón de Respomuso',         1, 2140,  9.40, 30.00),
('Ibón Azul (Lagos del Infierno)', 1, 2380, 1.20, 8.00),
('Ibón d''Anayet',            1, 2245,  2.10, NULL),        -- profundidad no publicada
('Ibón de Sabocos',           1, 2087,  NULL, NULL),        -- superficie y profundidad sin medir
('Ibón de los Baños de Panticosa', 5, 1630, NULL, 3.50),
-- Jacetania
('Ibón de Estanés',           2, 1754,  8.90, 15.50),
('Ibón de Ip',                2, 1910,  1.80, 7.20),
('Ibón de Acherito',          2, 1798,  NULL, NULL),        -- ibón occidental, datos limitados
-- Sobrarbe
('Ibón de Marboré',           3, 2612,  5.30, 20.00),
('Ibones de la Munia',        3, 2500,  3.00, 10.00),
('Ibón de Plan (Basa de la Mora)', 3, 1700, 3.50, 14.00),
-- Ribagorza
('Ibón de Billamuerta',       6, 2417,  NULL, NULL);        -- valle de Benasque, sin datos morfométricos públicos

-- ============================================================
-- TABLA: rutas
-- ============================================================

CREATE TABLE rutas (
    ruta_id             SERIAL PRIMARY KEY,
    nombre              VARCHAR(120) NOT NULL,
    comarca_id          INTEGER NOT NULL REFERENCES comarcas(comarca_id),
    distancia_km        NUMERIC(5,2) NOT NULL CHECK (distancia_km > 0),
    desnivel_m          INTEGER CHECK (desnivel_m >= 0),   -- ahora nullable: no siempre está medido con precisión
    duracion_horas      NUMERIC(4,2),                       -- ahora nullable: rutas recién añadidas sin cronometrar
    dificultad          nivel_dificultad NOT NULL,
    circular            BOOLEAN NOT NULL DEFAULT false,
    fecha_publicacion   DATE DEFAULT CURRENT_DATE           -- nullable: borradores aún sin publicar
);

INSERT INTO rutas (nombre, comarca_id, distancia_km, desnivel_m, duracion_horas, dificultad, circular, fecha_publicacion) VALUES
('Ruta al Ibón de Piedrafita',            1, 6.50, 350, 3.00, 'facil', true, '2024-06-10'),
('Circo de Piedrafita - Bachimaña',       1, 14.00, 950, 6.50, 'dificil', true, '2024-07-02'),
('Ruta a los Ibones de Respomuso',        1, 12.30, 700, 5.50, 'moderada', false, '2024-07-15'),
('Ascensión al Ibón Azul (Lagos del Infierno)', 1, 16.00, 1200, 7.00, 'muy_dificil', false, '2024-08-01'),
('Ruta al Ibón d''Anayet desde Formigal', 1, 10.50, 550, 4.50, 'moderada', false, '2024-06-25'),
('Ruta al Ibón de Sabocos',               1, 9.00, NULL, NULL, 'moderada', true, NULL),                  -- ruta recién trazada, sin publicar aún
('Paseo al Ibón de los Baños de Panticosa', 5, 4.00, 180, 2.00, 'facil', false, '2024-05-18'),
('Ruta al Ibón de Estanés',               2, 9.80, 490, 4.00, 'moderada', true, '2024-05-20'),
('Vuelta al Ibón de Ip',                  2, 8.20, 420, 3.50, 'facil', true, '2024-05-05'),
('Ruta al Ibón de Acherito desde Guarrinza', 2, 19.00, 700, 6.00, 'dificil', false, '2024-08-18'),
('Ruta a Marboré desde Bujaruelo',        3, 18.00, 1400, 8.00, 'muy_dificil', false, '2024-08-10'),
('Ibones de la Munia por Barrosa',        3, 15.50, 1100, 7.50, 'dificil', false, '2024-08-20'),
('Ruta a la Basa de la Mora (Ibón de Plan)', 3, 7.00, NULL, 3.20, 'facil', true, '2024-06-15'),          -- desnivel pendiente de medir con GPS
('Cañón de Añisclo (sin ibón)',           3, 13.00, 600, 5.00, 'moderada', false, '2024-07-30'),
('Barranco de la Peonera',                4, 5.00, 250, 3.00, 'moderada', false, '2024-05-12'),
('Ibones de Billamuerta desde La Besurta', 6, 11.00, 650, NULL, 'dificil', false, NULL);                 -- borrador, aún sin cronometrar ni publicar

-- ============================================================
-- TABLA INTERMEDIA: ruta_ibon (relación N:M)
-- Una ruta puede pasar por varios ibones y viceversa
-- ============================================================

CREATE TABLE ruta_ibon (
    ruta_id      INTEGER NOT NULL REFERENCES rutas(ruta_id) ON DELETE CASCADE,
    ibon_id      INTEGER NOT NULL REFERENCES ibones(ibon_id) ON DELETE CASCADE,
    orden_visita INTEGER DEFAULT 1,
    PRIMARY KEY (ruta_id, ibon_id)
);

INSERT INTO ruta_ibon (ruta_id, ibon_id, orden_visita) VALUES
(1, 1, 1),
(2, 1, 1), (2, 2, 2),
(3, 3, 1),
(4, 4, 1),
(5, 5, 1),
(6, 6, 1),
(7, 7, 1),
(8, 8, 1),
(9, 9, 1),
(10, 10, 1),
(11, 11, 1),
(12, 12, 1),
(13, 13, 1),
(16, 14, 1);

-- ============================================================
-- TABLA: resenas (para practicar agregaciones y JOINs con datos "de usuarios")
-- ============================================================

CREATE TABLE resenas (
    resena_id       SERIAL PRIMARY KEY,
    ruta_id         INTEGER NOT NULL REFERENCES rutas(ruta_id) ON DELETE CASCADE,
    autor           VARCHAR(60) NOT NULL,
    puntuacion      SMALLINT NOT NULL CHECK (puntuacion BETWEEN 1 AND 5),
    comentario      TEXT,           -- nullable: valoraciones solo con nota, sin texto
    fecha_resena    DATE DEFAULT CURRENT_DATE
);

INSERT INTO resenas (ruta_id, autor, puntuacion, comentario, fecha_resena) VALUES
(1, 'Marta', 5, 'Ruta ideal para iniciarse, paisaje espectacular', '2024-06-20'),
(1, 'Javier', 4, 'Muy bonita pero concurrida en agosto', '2024-08-05'),
(1, 'Ana', 4, NULL, '2024-08-22'),                                        -- solo puntuó, sin comentario
(2, 'Laura', 5, 'Exigente pero merece muchísimo la pena', '2024-07-10'),
(3, 'Pablo', 4, 'Buen desnivel, ibones preciosos', '2024-07-22'),
(4, 'Nuria', 3, 'Muy dura, llevar buen calzado', '2024-08-15'),
(5, 'Iker', 5, NULL, '2024-07-05'),                                       -- sin comentario
(7, 'Carlos', 5, 'Perfecta para ir con niños', '2024-05-25'),
(8, 'Elena', 4, 'Vistas increíbles al Estanés', '2024-06-30'),
(9, 'Diego', 3, NULL, NULL),                                              -- ni comentario ni fecha (reseña importada sin metadatos)
(11, 'Sergio', 5, 'La mejor ruta que he hecho en el Pirineo', '2024-08-12'),
(12, 'Cristina', 4, 'Larga pero muy gratificante', '2024-08-25'),
(13, 'David', 5, 'Ideal para tarde de verano', '2024-06-18'),
(15, 'Marcos', 4, 'Cañones espectaculares aunque hay que reservar', '2024-08-02');
-- Nota: las rutas 6, 10, 14 y 16 se dejan sin reseñas a propósito -> practicar LEFT JOIN / rutas sin valorar

-- ============================================================
-- MÁS RESEÑAS: para practicar GROUP BY / HAVING con volumen real
-- (varios usuarios distintos opinando sobre las mismas rutas)
-- ============================================================

INSERT INTO resenas (ruta_id, autor, puntuacion, comentario, fecha_resena) VALUES
-- Ruta 1: Ruta al Ibón de Piedrafita (ya tenía 3 -> la dejamos como la más "popular")
(1, 'Sara', 5, 'Perfecta para un domingo con la familia', '2024-06-28'),
(1, 'Rubén', 3, 'Bien pero muy llena de gente en verano', '2024-07-14'),
(1, 'Lucía', 5, NULL, '2024-08-01'),
(1, 'Hugo', 4, 'Fácil y con vistas muy bonitas', '2024-09-02'),
(1, 'Paula', 5, 'La recomiendo para iniciarse en senderismo', '2025-06-10'),

-- Ruta 2: Circo de Piedrafita - Bachimaña
(2, 'Marcos', 4, 'Dura pero el circo glaciar merece la pena', '2024-07-20'),
(2, 'Alba', 5, 'La mejor ruta que he hecho este año', '2024-08-11'),
(2, 'Iván', 3, NULL, '2024-08-25'),
(2, 'Noelia', 4, 'Larga, llevar buen calzado y agua', '2025-07-05'),

-- Ruta 3: Ruta a los Ibones de Respomuso
(3, 'Raquel', 5, 'Ibones espectaculares, muy recomendable', '2024-07-30'),
(3, 'Óscar', 4, NULL, '2024-08-09'),
(3, 'Beatriz', 4, 'Buen desnivel, apta para nivel medio', '2025-06-22'),

-- Ruta 4: Ascensión al Ibón Azul
(4, 'Fernando', 2, 'Se me hizo demasiado dura, cuidado con el desnivel', '2024-08-16'),
(4, 'Cristina', 4, 'Exigente pero espectacular arriba', '2024-08-30'),
(4, 'Adrián', 5, NULL, '2025-07-19'),

-- Ruta 5: Ruta al Ibón d'Anayet desde Formigal
(5, 'Teresa', 5, 'El pico Anayet reflejado en el agua es una pasada', '2024-07-02'),
(5, 'Gonzalo', 4, 'Ruta muy fotogénica', '2024-08-14'),
(5, 'Marina', 3, NULL, '2025-06-28'),

-- Ruta 7: Paseo al Ibón de los Baños de Panticosa
(7, 'Andrea', 5, 'Ideal para ir con niños pequeños', '2024-06-05'),
(7, 'Jorge', 4, 'Corta y tranquila, muy accesible', '2024-07-22'),
(7, 'Silvia', 5, NULL, '2025-05-30'),
(7, 'Pau', 3, 'Se llena mucho en agosto', '2025-08-01'),

-- Ruta 8: Ruta al Ibón de Estanés
(8, 'Miguel', 5, 'Frontera con Francia, paisaje único', '2024-07-08'),
(8, 'Claudia', 4, NULL, '2024-08-19'),
(8, 'Xavier', 4, 'Muy transitada pero bonita', '2025-06-15'),

-- Ruta 9: Vuelta al Ibón de Ip
(9, 'Nerea', 5, 'Ruta corta y muy agradecida', '2024-06-12'),
(9, 'Álvaro', 3, NULL, '2024-08-03'),
(9, 'Yolanda', 4, 'Buena opción para tarde de verano', '2025-07-11'),

-- Ruta 11: Ruta a Marboré desde Bujaruelo
(11, 'Ricardo', 5, 'Increíble, de las mejores de Ordesa', '2024-08-22'),
(11, 'Patricia', 4, 'Muy larga, salir temprano', '2024-09-01'),
(11, 'Enrique', 5, NULL, '2025-07-28'),

-- Ruta 12: Ibones de la Munia por Barrosa
(12, 'Victoria', 4, 'Exigente pero con paisajes de alta montaña', '2024-08-27'),
(12, 'Damián', 5, NULL, '2025-08-05'),

-- Ruta 13: Ruta a la Basa de la Mora (Ibón de Plan)
(13, 'Isabel', 5, 'Preciosa y tranquila, poco masificada', '2024-06-25'),
(13, 'Tomás', 4, 'Fácil de hacer en familia', '2025-06-30'),
(13, 'Celia', 3, NULL, '2025-08-10'),

-- Ruta 15: Barranco de la Peonera
(15, 'Julián', 4, 'Divertido, buena opción de barranco fácil', '2024-05-30'),
(15, 'Rosa', 5, NULL, '2025-07-02');
-- Nota: rutas 6, 10, 14 y 16 se mantienen SIN reseñas a propósito
-- (borradores/sin publicar) -> siguen sirviendo para practicar HAVING COUNT(*) = 0 vía LEFT JOIN

-- ============================================================
-- ÍNDICES ÚTILES
-- ============================================================

CREATE INDEX idx_rutas_comarca ON rutas(comarca_id);
CREATE INDEX idx_ibones_comarca ON ibones(comarca_id);
CREATE INDEX idx_resenas_ruta ON resenas(ruta_id);

-- ============================================================
-- CONSULTAS DE EJEMPLO PARA PRACTICAR (comentadas)
-- ============================================================

-- 1. Rutas por comarca con su dificultad
-- SELECT r.nombre, c.nombre AS comarca, r.dificultad
-- FROM rutas r JOIN comarcas c ON r.comarca_id = c.comarca_id;

-- 2. Puntuación media por ruta (usando resenas)
-- SELECT r.nombre, ROUND(AVG(res.puntuacion), 2) AS media
-- FROM rutas r JOIN resenas res ON r.ruta_id = res.ruta_id
-- GROUP BY r.nombre
-- ORDER BY media DESC;

-- 3. Ibones por encima de 2000m ordenados por altitud
-- SELECT nombre, altitud_m FROM ibones WHERE altitud_m > 2000 ORDER BY altitud_m DESC;

-- 4. Rutas que visitan más de un ibón (usando ruta_ibon)
-- SELECT r.nombre, COUNT(ri.ibon_id) AS num_ibones
-- FROM rutas r JOIN ruta_ibon ri ON r.ruta_id = ri.ruta_id
-- GROUP BY r.nombre
-- HAVING COUNT(ri.ibon_id) > 1;

-- 5. Ranking de comarcas por distancia media de sus rutas
-- SELECT c.nombre, ROUND(AVG(r.distancia_km), 2) AS distancia_media
-- FROM comarcas c JOIN rutas r ON c.comarca_id = r.comarca_id
-- GROUP BY c.nombre
-- ORDER BY distancia_media DESC;

-- 6. Window function: ranking de rutas más duras por comarca
-- SELECT nombre, comarca_id, desnivel_m,
--        RANK() OVER (PARTITION BY comarca_id ORDER BY desnivel_m DESC) AS ranking
-- FROM rutas;

-- ============================================================
-- CONSULTAS PARA PRACTICAR NULOS ESPECÍFICAMENTE
-- ============================================================

-- 7. Rutas sin reseñas todavía (LEFT JOIN + IS NULL)
-- SELECT r.nombre
-- FROM rutas r LEFT JOIN resenas res ON r.ruta_id = res.ruta_id
-- WHERE res.resena_id IS NULL;

-- 8. Ibones sin dato de profundidad, sustituyendo con COALESCE
-- SELECT nombre, COALESCE(profundidad_m::TEXT, 'sin datos') AS profundidad
-- FROM ibones;

-- 9. Cuidado: AVG/SUM ignoran los NULL, pero COUNT(*) no
-- SELECT COUNT(*) AS total_rutas, COUNT(desnivel_m) AS rutas_con_desnivel
-- FROM rutas;

-- 10. Rutas sin fecha de publicación (borradores)
-- SELECT nombre FROM rutas WHERE fecha_publicacion IS NULL;