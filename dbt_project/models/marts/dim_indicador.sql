SELECT 1 AS indicador_id, 'tipo_cambio_usd_mxn' AS nombre, 'Tipo de cambio USD/MXN' AS descripcion, 'Banxico' AS
fuente, 'MXN por USD' AS unidad, 'diaria' AS frecuencia
UNION ALL SELECT 2, 'tasa_interes_tiie', 'Tasa de interés TIIE', 'Banxico', 'porcentaje', 'variable'
UNION ALL SELECT 3, 'inflacion_inpc', 'Inflación mensual INPC', 'Banxico', 'índice', 'mensual'
UNION ALL SELECT 4, 'igae', 'Indicador Global de Actividad Económica', 'INEGI', 'índice', 'mensual'
UNION ALL SELECT 5, 'desempleo', 'Población desocupada 15+ años', 'INEGI', 'miles de personas', 'trimestral'
UNION ALL SELECT 6, 'petroleo_wti', 'Precio del petróleo WTI', 'Yahoo Finance', 'USD por barril', 'diaria'
UNION ALL SELECT 7, 'ipc_bolsa_mx', 'IPC Bolsa Mexicana de Valores', 'Yahoo Finance', 'puntos', 'diaria'
UNION ALL SELECT 8, 'oro', 'Precio del oro', 'Yahoo Finance', 'USD por onza', 'diaria'