-- Limpia los datos de población desocupada de INEGI

SELECT
    TO_DATE(time_period || '/01', 'YYYY/MM/DD') AS fecha,

    CAST(obs_value AS NUMERIC) AS desempleo_valor,

    fecha_extraccion

FROM {{ source('raw', 'inegi_desempleo') }}

WHERE obs_value IS NOT NULL
  AND obs_value != ''