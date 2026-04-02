import requests
import logging

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.utils.helpers import obtener_variable, guardar_json, configurar_logging

# Indicadores de INEGI y su nombre descriptivo
INDICADORES_INEGI = {
    "6207136901": "igae",
    "6200093973": "desempleo"
}

URL_BASE = "https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR"


def extraer_indicador(indicador_id, token):

    url = f"{URL_BASE}/{indicador_id}/es/00/false/BISE/2.0/{token}?type=json"
    nombre = INDICADORES_INEGI[indicador_id]

    logging.info(f"Extrayendo indicador {indicador_id} ({nombre})")

    try:
        respuesta = requests.get(url, timeout=60)
        respuesta.raise_for_status()

        datos_json = respuesta.json()
        observaciones = datos_json["Series"][0]["OBSERVATIONS"]

        logging.info(f"Indicador {indicador_id}: {len(observaciones)} registros obtenidos")
        return observaciones

    except requests.exceptions.Timeout:
        logging.error(f"Indicador {indicador_id}: La API tardó más de 60 segundos")
        return []
    except requests.exceptions.HTTPError as e:
        logging.error(f"Indicador {indicador_id}: Error HTTP {e}")
        return []
    except (KeyError, IndexError) as e:
        logging.error(f"Indicador {indicador_id}: Estructura de respuesta inesperada - {e}")
        return []
    except Exception as e:
        logging.error(f"Indicador {indicador_id}: Error inesperado - {e}")
        return []


def extraer_inegi():

    configurar_logging("inegi")
    logging.info("=== Inicio extracción INEGI ===")

    token = obtener_variable("INEGI_TOKEN")

    resultados = {}
    indicadores_exitosos = 0

    for indicador_id, nombre in INDICADORES_INEGI.items():
        datos = extraer_indicador(indicador_id, token)
        if datos:
            resultados[nombre] = {
                "indicador_id": indicador_id,
                "registros": len(datos),
                "datos": datos
            }
            indicadores_exitosos += 1

    if resultados:
        ruta = guardar_json(resultados, "inegi")
        logging.info(f"=== Extracción INEGI completada: {indicadores_exitosos}/2 indicadores exitosos ===")
    else:
        logging.error("=== Extracción INEGI falló: no se obtuvieron datos ===")

    return resultados


if __name__ == "__main__":
    extraer_inegi()