-- ============================================================
-- BASE DE DATOS DE PRÁCTICA: EXCURSIONES E IBONES DEL PIRINEO
-- Autor: Adrián | Uso: práctica SQL en PostgreSQL
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
    descripcion     TEXT
);

INSERT INTO comarcas (nombre, provincia, descripcion) VALUES
('Valle de Tena', 'Huesca', 'Valle pirenaico famoso por Sallent de Gállego y Panticosa'),
('Jacetania', 'Huesca', 'Comarca del Pirineo occidental aragonés, capital Jaca'),
('Sobrarbe', 'Huesca', 'Comarca que alberga el Parque Nacional de Ordesa y Monte Perdido'),
('Sierra de Guara', 'Huesca', 'Conocida por barrancos y cañones, sur del Pirineo');

-- ============================================================
-- TABLA: ibones
-- ============================================================

CREATE TABLE ibones (
    ibon_id         SERIAL PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    comarca_id      INTEGER NOT NULL REFERENCES comarcas(comarca_id),
    altitud_m       INTEGER CHECK (altitud_m > 0),
    superficie_ha   NUMERIC(6,2),
    profundidad_m   NUMERIC(5,2)
);

INSERT INTO ibones (nombre, comarca_id, altitud_m, superficie_ha, profundidad_m) VALUES
('Ibón de Piedrafita', 1, 1635, 12.50, 12.00),
('Ibón de Bachimaña', 1, 2237, 6.80, 30.00),
('Ibón de Respomuso', 1, 2140, 9.40, 30.00),
('Ibón Azul', 1, 2400, 1.20, 8.00),
('Ibón de Estanés', 2, 1785, 8.90, 15.50),
('Ibón d''Anayet', 2, 2227, 2.10, 6.00),
('Ibón de Ip', 2, 2180, 1.80, 7.20),
('Ibón de Marboré', 3, 2612, 5.30, 20.00),
('Ibones de la Munia', 3, 2500, 3.00, 10.00),
('Ibón de Plan', 3, 1985, 2.40, 5.00);

-- ============================================================
-- TABLA: rutas
-- ============================================================

CREATE TABLE rutas (
    ruta_id             SERIAL PRIMARY KEY,
    nombre              VARCHAR(120) NOT NULL,
    comarca_id          INTEGER NOT NULL REFERENCES comarcas(comarca_id),
    distancia_km        NUMERIC(5,2) NOT NULL CHECK (distancia_km > 0),
    desnivel_m          INTEGER NOT NULL CHECK (desnivel_m >= 0),
    duracion_horas      NUMERIC(4,2) NOT NULL,
    dificultad          nivel_dificultad NOT NULL,
    circular            BOOLEAN NOT NULL DEFAULT false,
    fecha_publicacion   DATE DEFAULT CURRENT_DATE
);

INSERT INTO rutas (nombre, comarca_id, distancia_km, desnivel_m, duracion_horas, dificultad, circular, fecha_publicacion) VALUES
('Ruta al Ibón de Piedrafita', 1, 6.50, 350, 3.00, 'facil', true, '2024-06-10'),
('Circo de Piedrafita - Bachimaña', 1, 14.00, 950, 6.50, 'dificil', true, '2024-07-02'),
('Ruta a los Ibones de Respomuso', 1, 12.30, 700, 5.50, 'moderada', false, '2024-07-15'),
('Ascensión al Ibón Azul', 1, 16.00, 1200, 7.00, 'muy_dificil', false, '2024-08-01'),
('Ruta al Ibón de Estanés', 2, 9.80, 480, 4.00, 'moderada', true, '2024-05-20'),
('Ruta al Ibón d''Anayet', 2, 10.50, 550, 4.50, 'moderada', false, '2024-06-25'),
('Vuelta al Ibón de Ip', 2, 8.20, 420, 3.50, 'facil', true, '2024-05-05'),
('Ruta a Marboré desde Bujaruelo', 3, 18.00, 1400, 8.00, 'muy_dificil', false, '2024-08-10'),
('Ibones de la Munia por Barrosa', 3, 15.50, 1100, 7.50, 'dificil', false, '2024-08-20'),
('Ruta fácil al Ibón de Plan', 3, 7.00, 380, 3.20, 'facil', true, '2024-06-15'),
('Cañón de Añisclo (sin ibón)', 3, 13.00, 600, 5.00, 'moderada', false, '2024-07-30'),
('Barranco de la Peonera', 4, 5.00, 250, 3.00, 'moderada', false, '2024-05-12');

-- ============================================================
-- TABLA INTERMEDIA: ruta_ibon (relación N:M)
-- Una ruta puede pasar por varios ibones y viceversa
-- ============================================================

CREATE TABLE ruta_ibon (
    ruta_id     INTEGER NOT NULL REFERENCES rutas(ruta_id) ON DELETE CASCADE,
    ibon_id     INTEGER NOT NULL REFERENCES ibones(ibon_id) ON DELETE CASCADE,
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
(10, 10, 1);

-- ============================================================
-- TABLA: resenas (para practicar agregaciones y JOINs con datos "de usuarios")
-- ============================================================

CREATE TABLE resenas (
    resena_id       SERIAL PRIMARY KEY,
    ruta_id         INTEGER NOT NULL REFERENCES rutas(ruta_id) ON DELETE CASCADE,
    autor           VARCHAR(60) NOT NULL,
    puntuacion      SMALLINT NOT NULL CHECK (puntuacion BETWEEN 1 AND 5),
    comentario      TEXT,
    fecha_resena    DATE DEFAULT CURRENT_DATE
);

INSERT INTO resenas (ruta_id, autor, puntuacion, comentario, fecha_resena) VALUES
(1, 'Marta', 5, 'Ruta ideal para iniciarse, paisaje espectacular', '2024-06-20'),
(1, 'Javier', 4, 'Muy bonita pero concurrida en agosto', '2024-08-05'),
(2, 'Laura', 5, 'Exigente pero merece muchísimo la pena', '2024-07-10'),
(3, 'Pablo', 4, 'Buen desnivel, ibones preciosos', '2024-07-22'),
(4, 'Nuria', 3, 'Muy dura, llevar buen calzado', '2024-08-15'),
(5, 'Carlos', 5, 'Perfecta para ir con niños', '2024-05-25'),
(6, 'Elena', 4, 'Vistas increíbles al Anayet', '2024-06-30'),
(8, 'Sergio', 5, 'La mejor ruta que he hecho en el Pirineo', '2024-08-12'),
(9, 'Cristina', 4, 'Larga pero muy gratificante', '2024-08-25'),
(10, 'David', 5, 'Ideal para tarde de verano', '2024-06-18');

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