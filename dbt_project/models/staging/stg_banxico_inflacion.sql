SELECT
    TO_DATE(fecha, 'DD/MM/YYYY') AS fecha,
    CAST(dato AS NUMERIC) AS inflacion_inpc,
    fecha_extraccion

FROM {{ source('raw', 'banxico_inflacion') }}

WHERE dato != 'N/E'
  AND dato IS NOT NULL
  AND dato != ''