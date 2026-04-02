CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS intermediate;
CREATE SCHEMA IF NOT EXISTS marts;

CREATE TABLE IF NOT EXISTS raw.banxico_tipo_cambio (
    id SERIAL PRIMARY KEY,
    fecha TEXT NOT NULL,
    dato TEXT,
    fecha_extraccion TIMESTAMP DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS raw.banxico_tasa_interes (
    id SERIAL PRIMARY KEY,
    fecha TEXT NOT NULL,
    dato TEXT,
    fecha_extraccion TIMESTAMP DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS raw.banxico_inflacion (
    id SERIAL PRIMARY KEY,
    fecha TEXT NOT NULL,
    dato TEXT,
    fecha_extraccion TIMESTAMP DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS raw.inegi_igae (
    id SERIAL PRIMARY KEY,
    time_period TEXT NOT NULL,
    obs_value TEXT,
    fecha_extraccion TIMESTAMP DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS raw.inegi_desempleo (
    id SERIAL PRIMARY KEY,
    time_period TEXT NOT NULL,
    obs_value TEXT,
    fecha_extraccion TIMESTAMP DEFAULT NOW()
);



CREATE TABLE IF NOT EXISTS raw.yahoo_petroleo (
    id SERIAL PRIMARY KEY,
    fecha TEXT NOT NULL,
    open_price TEXT,
    high TEXT,
    low TEXT,
    close_price TEXT,
    volume TEXT,
    fecha_extraccion TIMESTAMP DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS raw.yahoo_ipc_bolsa (
    id SERIAL PRIMARY KEY,
    fecha TEXT NOT NULL,
    open_price TEXT,
    high TEXT,
    low TEXT,
    close_price TEXT,
    volume TEXT,
    fecha_extraccion TIMESTAMP DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS raw.yahoo_oro (
    id SERIAL PRIMARY KEY,
    fecha TEXT NOT NULL,
    open_price TEXT,
    high TEXT,
    low TEXT,
    close_price TEXT,
    volume TEXT,
    fecha_extraccion TIMESTAMP DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS raw.opensky_trafico (
    id SERIAL PRIMARY KEY,
    fecha TEXT NOT NULL,
    total_aviones TEXT,
    en_vuelo TEXT,
    en_tierra TEXT,
    velocidad_promedio TEXT,
    altitud_promedio TEXT,
    pais_mas_frecuente TEXT,
    fecha_extraccion TIMESTAMP DEFAULT NOW()
);