SELECT
    fecha,
    indicador,
    valor,
    fuente,

    -- LAG(valor, 1): toma el valor de la fila anterior
    LAG(valor, 1) OVER (
        PARTITION BY indicador
        ORDER BY fecha
    ) AS valor_anterior,

    -- Variación porcentual
    ROUND(
        (
            (
                valor
                - LAG(valor, 1) OVER (
                    PARTITION BY indicador
                    ORDER BY fecha
                )
            )
            / NULLIF(
                LAG(valor, 1) OVER (
                    PARTITION BY indicador
                    ORDER BY fecha
                ),
                0
            )
        ) * 100,
        4
    ) AS variacion_porcentual,

    -- Promedio móvil 7 días
    ROUND(
        AVG(valor) OVER (
            PARTITION BY indicador
            ORDER BY fecha
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ),
        4
    ) AS promedio_movil_7d,

    -- Promedio móvil 30 días
    ROUND(
        AVG(valor) OVER (
            PARTITION BY indicador
            ORDER BY fecha
            ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
        ),
        4
    ) AS promedio_movil_30d

FROM {{ ref('int_indicadores_diarios') }}