import requests
import logging
from datetime import datetime, timedelta

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.utils.helpers import obtener_variable, guardar_json, configurar_logging

# Las series que vamos a extraer y qué significa cada una
SERIES_BANXICO = {
    "SF43718": "tipo_cambio_usd_mxn",
    "SF61745": "tasa_tiie",
    "SP1": "inflacion_mensual"
}

URL_BASE = "https://www.banxico.org.mx/SieAPIRest/service/v1/series"


def extraer_serie(serie_id, token, fecha_inicio, fecha_fin):

    url = f"{URL_BASE}/{serie_id}/datos/{fecha_inicio}/{fecha_fin}"
    params = {"token": token}

    logging.info(f"Extrayendo serie {serie_id} ({SERIES_BANXICO[serie_id]})")

    try:
        respuesta = requests.get(url, params=params, timeout=30)
        respuesta.raise_for_status()

        datos_json = respuesta.json()
        datos = datos_json["bmx"]["series"][0]["datos"]

        logging.info(f"Serie {serie_id}: {len(datos)} registros obtenidos")
        return datos

    except requests.exceptions.Timeout:
        logging.error(f"Serie {serie_id}: La API tardó más de 30 segundos en responder")
        return []
    except requests.exceptions.HTTPError as e:
        logging.error(f"Serie {serie_id}: Error HTTP {e}")
        return []
    except KeyError as e:
        logging.error(f"Serie {serie_id}: Estructura de respuesta inesperada - {e}")
        return []
    except Exception as e:
        logging.error(f"Serie {serie_id}: Error inesperado - {e}")
        return []


def extraer_banxico():

    configurar_logging("banxico")
    logging.info("=== Inicio extracción Banxico ===")

    token = obtener_variable("BANXICO_TOKEN")

    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=365)

    fecha_inicio_str = fecha_inicio.strftime("%Y-%m-%d")
    fecha_fin_str = fecha_fin.strftime("%Y-%m-%d")

    logging.info(f"Rango: {fecha_inicio_str} a {fecha_fin_str}")

    resultados = {}
    series_exitosas = 0

    for serie_id, nombre in SERIES_BANXICO.items():
        datos = extraer_serie(serie_id, token, fecha_inicio_str, fecha_fin_str)
        if datos:
            resultados[nombre] = {
                "serie_id": serie_id,
                "registros": len(datos),
                "datos": datos
            }
            series_exitosas += 1

    # Guardar resultados en JSON
    if resultados:
        ruta = guardar_json(resultados, "banxico")
        logging.info(f"=== Extracción Banxico completada: {series_exitosas}/3 series exitosas ===")
    else:
        logging.error("=== Extracción Banxico falló: no se obtuvieron datos ===")

    return resultados


if __name__ == "__main__":
    extraer_banxico()