SELECT 1 AS fuente_id, 'Banxico' AS nombre, 'https://www.banxico.org.mx/SieAPIRest/service/v1/' AS url_api, 'Banco de
México - Indicadores económicos oficiales' AS descripcion, TRUE AS requiere_token
UNION ALL SELECT 2, 'INEGI', 'https://www.inegi.org.mx/app/api/indicadores/', 'Instituto Nacional de Estadística y
Geografía', TRUE
UNION ALL SELECT 3, 'Yahoo Finance', 'https://finance.yahoo.com/', 'Datos de mercados financieros globales', FALSE
UNION ALL SELECT 4, 'OpenSky', 'https://opensky-network.org/api/', 'Red de rastreo de tráfico aéreo en tiempo real',
FALSE