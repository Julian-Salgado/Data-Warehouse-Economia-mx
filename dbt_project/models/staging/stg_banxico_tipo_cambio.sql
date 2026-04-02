SELECT
    TO_DATE(fecha, 'DD/MM/YYYY') AS fecha,
    CAST(dato AS NUMERIC) AS tipo_cambio,
    fecha_extraccion

FROM {{ source('raw', 'banxico_tipo_cambio') }}

WHERE dato != 'N/E'
  AND dato IS NOT NULL
  AND dato != ''