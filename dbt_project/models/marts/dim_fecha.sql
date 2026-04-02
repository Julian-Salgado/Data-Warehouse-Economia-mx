WITH rango_fechas AS (
    SELECT
        MIN(fecha) AS fecha_min,
        MAX(fecha) AS fecha_max
    FROM {{ ref('int_indicadores_diarios') }}
),

-- generate_series crea una secuencia de fechas
todas_las_fechas AS (
    SELECT
        generate_series(
            fecha_min,
            fecha_max,
            '1 day'::interval
        )::date AS fecha
    FROM rango_fechas
)

SELECT
    fecha,
    EXTRACT(YEAR FROM fecha)::INTEGER AS anio,
    EXTRACT(MONTH FROM fecha)::INTEGER AS mes,
    EXTRACT(DAY FROM fecha)::INTEGER AS dia,

    -- 0=domingo, 1=lunes, ..., 6=sábado
    EXTRACT(DOW FROM fecha)::INTEGER AS dia_semana,

    TO_CHAR(fecha, 'TMMonth') AS nombre_mes,
    EXTRACT(QUARTER FROM fecha)::INTEGER AS trimestre,

    -- Fin de semana
    CASE
        WHEN EXTRACT(DOW FROM fecha) IN (0, 6) THEN TRUE
        ELSE FALSE
    END AS es_fin_de_semana,

    -- Días festivos (simplificado)
    CASE
        WHEN EXTRACT(MONTH FROM fecha) = 1 AND EXTRACT(DAY FROM fecha) = 1 THEN TRUE
        WHEN EXTRACT(MONTH FROM fecha) = 2 AND EXTRACT(DAY FROM fecha) = 5 THEN TRUE
        WHEN EXTRACT(MONTH FROM fecha) = 3 AND EXTRACT(DAY FROM fecha) = 21 THEN TRUE
        WHEN EXTRACT(MONTH FROM fecha) = 5 AND EXTRACT(DAY FROM fecha) = 1 THEN TRUE
        WHEN EXTRACT(MONTH FROM fecha) = 9 AND EXTRACT(DAY FROM fecha) = 16 THEN TRUE
        WHEN EXTRACT(MONTH FROM fecha) = 11 AND EXTRACT(DAY FROM fecha) = 20 THEN TRUE
        WHEN EXTRACT(MONTH FROM fecha) = 12 AND EXTRACT(DAY FROM fecha) = 25 THEN TRUE
        ELSE FALSE
    END AS es_dia_festivo

FROM todas_las_fechas