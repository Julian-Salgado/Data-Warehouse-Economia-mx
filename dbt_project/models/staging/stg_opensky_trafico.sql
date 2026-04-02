SELECT
    CAST(fecha AS DATE) AS fecha,
    CAST(total_aviones AS INTEGER) AS total_aviones,
    CAST(en_vuelo AS INTEGER) AS en_vuelo,
    CAST(en_tierra AS INTEGER) AS en_tierra,
    CAST(velocidad_promedio AS NUMERIC) AS velocidad_promedio,
    CAST(altitud_promedio AS NUMERIC) AS altitud_promedio,
    pais_mas_frecuente,
    fecha_extraccion

FROM {{ source('raw', 'opensky_trafico') }}

WHERE total_aviones IS NOT NULL
  AND total_aviones != ''