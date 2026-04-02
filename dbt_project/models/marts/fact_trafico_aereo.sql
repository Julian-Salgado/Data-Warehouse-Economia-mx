SELECT
    ROW_NUMBER() OVER (
        ORDER BY t.fecha
    ) AS id,

    t.fecha,

    -- OpenSky siempre es fuente_id = 4
    f.fuente_id,

    t.total_aviones,
    t.en_vuelo,
    t.en_tierra,
    t.velocidad_promedio,
    t.altitud_promedio,
    t.pais_mas_frecuente

FROM {{ ref('int_trafico_aereo_diario') }} t

LEFT JOIN {{ ref('dim_fuente') }} f
    ON t.fuente = f.nombre