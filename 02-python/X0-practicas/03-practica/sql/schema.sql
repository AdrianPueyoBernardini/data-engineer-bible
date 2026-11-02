DROP TABLE IF EXISTS resumen_importacion;
DROP TABLE IF EXISTS plan_viaje;
DROP TABLE IF EXISTS ruta;

CREATE TABLE ruta (
    id            SERIAL PRIMARY KEY,
    id_ruta       TEXT NOT NULL UNIQUE,
    nombre        TEXT NOT NULL,
    distancia_km  NUMERIC(6,2) NOT NULL CHECK (distancia_km > 0),
    desnivel_m    INTEGER CHECK (desnivel_m >= 0),
    valle         TEXT NOT NULL,
    dificultad    TEXT NOT NULL
);

CREATE TABLE plan_viaje (
    id            SERIAL PRIMARY KEY,
    id_plan       TEXT NOT NULL UNIQUE,
    ruta_id       INTEGER NOT NULL REFERENCES ruta(id),
    fecha_inicio  DATE NOT NULL,
    fecha_fin     DATE NOT NULL,
    estado        TEXT NOT NULL,
    CHECK (fecha_fin >= fecha_inicio)
);

CREATE TABLE resumen_importacion (
    id            SERIAL PRIMARY KEY,
    id_operacion  TEXT NOT NULL UNIQUE,
    fecha         TIMESTAMPTZ NOT NULL DEFAULT now(),
    nuevos        INTEGER NOT NULL CHECK (nuevos >= 0),
    duplicados    INTEGER NOT NULL CHECK (duplicados >= 0),
    conflictos    INTEGER NOT NULL CHECK (conflictos >= 0),
    rechazados    INTEGER NOT NULL CHECK (rechazados >= 0)
);