SELECT
    fecha,
    'tipo_cambio_usd_mxn' AS indicador,
    tipo_cambio AS valor,
    'Banxico' AS fuente
FROM {{ ref('stg_banxico_tipo_cambio') }}

UNION ALL

SELECT
    fecha,
    'tasa_interes_tiie' AS indicador,
    tasa_interes AS valor,
    'Banxico' AS fuente
FROM {{ ref('stg_banxico_tasa_interes') }}

UNION ALL

SELECT
    fecha,
    'inflacion_inpc' AS indicador,
    inflacion_inpc AS valor,
    'Banxico' AS fuente
FROM {{ ref('stg_banxico_inflacion') }}

UNION ALL

SELECT
    fecha,
    'igae' AS indicador,
    igae_valor AS valor,
    'INEGI' AS fuente
FROM {{ ref('stg_inegi_igae') }}

UNION ALL

SELECT
    fecha,
    'desempleo' AS indicador,
    desempleo_valor AS valor,
    'INEGI' AS fuente
FROM {{ ref('stg_inegi_desempleo') }}

UNION ALL

SELECT
    fecha,
    'petroleo_wti' AS indicador,
    precio_cierre AS valor,
    'Yahoo Finance' AS fuente
FROM {{ ref('stg_yahoo_petroleo') }}

UNION ALL

SELECT
    fecha,
    'ipc_bolsa_mx' AS indicador,
    precio_cierre AS valor,
    'Yahoo Finance' AS fuente
FROM {{ ref('stg_yahoo_ipc_bolsa') }}

UNION ALL

SELECT
    fecha,
    'oro' AS indicador,
    precio_cierre AS valor,
    'Yahoo Finance' AS fuente
FROM {{ ref('stg_yahoo_oro') }}