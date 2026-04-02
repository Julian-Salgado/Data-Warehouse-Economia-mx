SELECT
    -- ROW_NUMBER genera un ID único para cada fila
    ROW_NUMBER() OVER (
        ORDER BY v.fecha, v.indicador
    ) AS id,

    v.fecha,

    -- Obtener indicador_id
    i.indicador_id,

    -- Obtener fuente_id
    f.fuente_id,

    v.valor,
    v.valor_anterior,
    v.variacion_porcentual,
    v.promedio_movil_7d,
    v.promedio_movil_30d

FROM {{ ref('int_indicadores_con_variaciones') }} v

-- JOIN con dim_indicador
LEFT JOIN {{ ref('dim_indicador') }} i
    ON v.indicador = i.nombre

-- JOIN con dim_fuente
LEFT JOIN {{ ref('dim_fuente') }} f
    ON v.fuente = f.nombre