import yfinance as yf
import logging

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from src.utils.helpers import guardar_json, configurar_logging

# Símbolos a extraer y su nombre descriptivo
SIMBOLOS_YAHOO = {
    "CL=F": "petroleo_wti",
    "^MXX": "ipc_bolsa_mx",
    "GC=F": "oro"
}


def extraer_simbolo(simbolo, nombre, periodo="1y"):

    logging.info(f"Extrayendo {simbolo} ({nombre})")

    try:
        datos = yf.download(simbolo, period=periodo, progress=False)

        if datos.empty:
            logging.error(f"{simbolo}: No se obtuvieron datos")
            return []

        # Convertir DataFrame a lista de diccionarios
        registros = []
        for fecha, fila in datos.iterrows():
            registro = {
                "fecha": fecha.strftime("%Y-%m-%d"),
                "open": round(float(fila[("Open", simbolo)]), 4),
                "high": round(float(fila[("High", simbolo)]), 4),
                "low": round(float(fila[("Low", simbolo)]), 4),
                "close": round(float(fila[("Close", simbolo)]), 4),
                "volume": int(fila[("Volume", simbolo)])
            }
            registros.append(registro)

        logging.info(f"{simbolo}: {len(registros)} registros obtenidos")
        return registros

    except Exception as e:
        logging.error(f"{simbolo}: Error inesperado - {e}")
        return []


def extraer_yahoo():
    """
    Función principal que extrae todos los símbolos de Yahoo Finance.
    """
    configurar_logging("yahoo")
    logging.info("=== Inicio extracción Yahoo Finance ===")

    resultados = {}
    simbolos_exitosos = 0

    for simbolo, nombre in SIMBOLOS_YAHOO.items():
        datos = extraer_simbolo(simbolo, nombre)
        if datos:
            resultados[nombre] = {
                "simbolo": simbolo,
                "registros": len(datos),
                "datos": datos
            }
            simbolos_exitosos += 1

    if resultados:
        ruta = guardar_json(resultados, "yahoo")
        logging.info(f"=== Extracción Yahoo completada: {simbolos_exitosos}/3 símbolos exitosos ===")
    else:
        logging.error("=== Extracción Yahoo falló: no se obtuvieron datos ===")

    return resultados


if __name__ == "__main__":
    extraer_yahoo()