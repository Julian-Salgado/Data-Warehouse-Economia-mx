-- Limpia los datos crudos de la tasa de interés TIIE de Banxico

SELECT
    TO_DATE(fecha, 'DD/MM/YYYY') AS fecha,
    CAST(dato AS NUMERIC) AS tasa_interes,
    fecha_extraccion

FROM {{ source('raw', 'banxico_tasa_interes') }}

WHERE dato != 'N/E'
  AND dato IS NOT NULL
  AND dato != ''