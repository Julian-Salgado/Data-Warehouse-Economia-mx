SELECT
    fecha,
    total_aviones,
    en_vuelo,
    en_tierra,
    velocidad_promedio,
    altitud_promedio,
    pais_mas_frecuente,
    'OpenSky' AS fuente

FROM {{ ref('stg_opensky_trafico') }}