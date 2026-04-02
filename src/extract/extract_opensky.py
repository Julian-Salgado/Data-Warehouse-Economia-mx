import requests
import logging

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.utils.helpers import guardar_json, configurar_logging

# Coordenadas del espacio aéreo de México
MEXICO_BOUNDS = {
    "lamin": 14.5,
    "lamax": 32.7,
    "lomin": -118.4,
    "lomax": -86.7
}

URL_OPENSKY = "https://opensky-network.org/api/states/all"


def extraer_opensky():

    configurar_logging("opensky")
    logging.info("=== Inicio extracción OpenSky ===")

    try:
        logging.info("Consultando aviones sobre México...")
        respuesta = requests.get(URL_OPENSKY, params=MEXICO_BOUNDS, timeout=30)
        respuesta.raise_for_status()

        datos_json = respuesta.json()
        aviones = datos_json.get("states", [])

        if not aviones:
            logging.warning("No se encontraron aviones sobre México")
            return {}

        # Procesar cada avión
        registros = []
        en_vuelo = 0
        en_tierra = 0
        velocidades = []
        altitudes = []
        paises = {}

        for avion in aviones:
            pais = avion[2] if avion[2] else "Desconocido"
            en_ground = avion[8] if avion[8] is not None else False
            velocidad = avion[9] if avion[9] is not None else 0
            altitud = avion[7] if avion[7] is not None else 0

            if en_ground:
                en_tierra += 1
            else:
                en_vuelo += 1

            if velocidad > 0:
                velocidades.append(velocidad * 3.6)  # m/s a km/h

            if altitud > 0:
                altitudes.append(altitud)

            paises[pais] = paises.get(pais, 0) + 1

            registros.append({
                "icao24": avion[0],
                "callsign": avion[1].strip() if avion[1] else None,
                "pais_origen": pais,
                "en_tierra": en_ground,
                "velocidad_ms": velocidad,
                "altitud_m": altitud
            })

        # País más frecuente
        pais_mas_frecuente = max(paises, key=paises.get)

        # Resumen
        resumen = {
            "total_aviones": len(aviones),
            "en_vuelo": en_vuelo,
            "en_tierra": en_tierra,
            "velocidad_promedio_kmh": round(sum(velocidades) / len(velocidades), 2) if velocidades else 0,
            "altitud_promedio_m": round(sum(altitudes) / len(altitudes), 2) if altitudes else 0,
            "pais_mas_frecuente": pais_mas_frecuente,
            "distribucion_paises": paises,
            "aviones": registros
        }

        ruta = guardar_json(resumen, "opensky")
        logging.info(f"Total aviones: {len(aviones)} | En vuelo: {en_vuelo} | En tierra: {en_tierra}")
        logging.info(f"Velocidad promedio: {resumen['velocidad_promedio_kmh']} km/h")
        logging.info(f"País más frecuente: {pais_mas_frecuente} ({paises[pais_mas_frecuente]} aviones)")
        logging.info("=== Extracción OpenSky completada ===")

        return resumen

    except requests.exceptions.Timeout:
        logging.error("La API tardó más de 30 segundos en responder")
        return {}
    except requests.exceptions.HTTPError as e:
        logging.error(f"Error HTTP: {e}")
        return {}
    except Exception as e:
        logging.error(f"Error inesperado: {e}")
        return {}


if __name__ == "__main__":
    extraer_opensky()