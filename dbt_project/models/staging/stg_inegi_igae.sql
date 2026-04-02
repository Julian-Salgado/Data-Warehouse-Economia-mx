-- Limpia los datos del Indicador Global de Actividad Económica (IGAE)

SELECT
    TO_DATE(time_period || '/01', 'YYYY/MM/DD') AS fecha,

    CAST(obs_value AS NUMERIC) AS igae_valor,

    fecha_extraccion

FROM {{ source('raw', 'inegi_igae') }}

WHERE obs_value IS NOT NULL
  AND obs_value != ''