SELECT
    CAST(fecha AS DATE) AS fecha,
    CAST(open_price AS NUMERIC) AS precio_apertura,
    CAST(high AS NUMERIC) AS precio_maximo,
    CAST(low AS NUMERIC) AS precio_minimo,
    CAST(close_price AS NUMERIC) AS precio_cierre,
    CAST(volume AS NUMERIC) AS volumen,
    fecha_extraccion

FROM {{ source('raw', 'yahoo_ipc_bolsa') }}

WHERE close_price IS NOT NULL
  AND close_price != ''