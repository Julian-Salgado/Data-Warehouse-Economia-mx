import json
import os
import sys
import logging
from datetime import datetime
import psycopg2
from dotenv import load_dotenv

load_dotenv()

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

fecha_hoy = datetime.now().strftime("%Y%m%d")
log_file = os.path.join(log_dir, f"load_raw_{fecha_hoy}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def conectar_postgresql():

    try:
        conexion = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            dbname=os.getenv("POSTGRES_DB", "data_warehouse_economia"),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD")
        )
        logger.info("Conexión a PostgreSQL exitosa")
        return conexion

    except Exception as e:
        logger.error(f"Error al conectar a PostgreSQL: {e}")
        sys.exit(1)


def leer_json(nombre_fuente):

    carpeta = "data"

    archivos = [
        f for f in os.listdir(carpeta)
        if f.startswith(nombre_fuente) and f.endswith(".json")
    ]

    if not archivos:
        logger.warning(f"No se encontró archivo JSON para {nombre_fuente}")
        return None

    archivos.sort()
    archivo = archivos[-1]
    ruta = os.path.join(carpeta, archivo)

    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)

    logger.info(f"Archivo leído: {ruta}")
    return datos


def cargar_banxico(conexion):

    datos = leer_json("banxico")
    if not datos:
        return

    mapeo_tablas = {
        "tipo_cambio_usd_mxn": "raw.banxico_tipo_cambio",
        "tasa_tiie": "raw.banxico_tasa_interes",
        "inflacion_mensual": "raw.banxico_inflacion"
    }

    cursor = conexion.cursor()
    total_insertados = 0

    for serie, contenido in datos.items():
        tabla = mapeo_tablas.get(serie)
        if not tabla:
            logger.warning(f"Serie desconocida: {serie}")
            continue

        registros = contenido.get("datos", [])
        insertados = 0
        for registro in registros:
            fecha = registro.get("fecha", "")
            dato = registro.get("dato", "")

            cursor.execute(
                f"SELECT 1 FROM {tabla} WHERE fecha = %s AND dato = %s",
                (fecha, dato)
            )

            if cursor.fetchone() is None:
                cursor.execute(
                    f"INSERT INTO {tabla} (fecha, dato) VALUES (%s, %s)",
                    (fecha, dato)
                )
                insertados += 1

        logger.info(
            f"{tabla}: {insertados} insertados ({len(registros)} en archivo)"
        )

        total_insertados += insertados

    conexion.commit()
    logger.info(f"Banxico: {total_insertados} nuevos registros")


def cargar_inegi(conexion):

    datos = leer_json("inegi")
    if not datos:
        return

    mapeo_tablas = {
        "igae": "raw.inegi_igae",
        "desempleo": "raw.inegi_desempleo"
    }

    cursor = conexion.cursor()
    total_insertados = 0

    for codigo, contenido in datos.items():
        tabla = mapeo_tablas.get(codigo)
        if not tabla:
            logger.warning(f"Código desconocido: {codigo}")
            continue

        registros = contenido.get("datos", [])
        insertados = 0
        for registro in registros:
            time_period = registro.get("TIME_PERIOD", "")
            obs_value = registro.get("OBS_VALUE", "")

            cursor.execute(
                f"""SELECT 1 FROM {tabla}
                WHERE time_period = %s AND obs_value = %s""",
                (time_period, obs_value)
            )

            if cursor.fetchone() is None:
                cursor.execute(
                    f"""INSERT INTO {tabla} (time_period, obs_value)
                    VALUES (%s, %s)""",
                    (time_period, obs_value)
                )
                insertados += 1

        logger.info(
            f"{tabla}: {insertados} insertados ({len(registros)} en archivo)"
        )

        total_insertados += insertados

    conexion.commit()
    logger.info(f"INEGI: {total_insertados} nuevos registros")


def cargar_yahoo(conexion):

    datos = leer_json("yahoo")
    if not datos:
        return

    mapeo_tablas = {
        "petroleo_wti": "raw.yahoo_petroleo",
        "ipc_bolsa_mx": "raw.yahoo_ipc_bolsa",
        "oro": "raw.yahoo_oro"
    }

    cursor = conexion.cursor()
    total_insertados = 0

    for simbolo, contenido in datos.items():
        tabla = mapeo_tablas.get(simbolo)
        if not tabla:
            logger.warning(f"Símbolo desconocido: {simbolo}")
            continue

        registros = contenido.get("datos", [])
        insertados = 0
        for registro in registros:
            fecha = registro.get("fecha", "")

            cursor.execute(
                f"SELECT 1 FROM {tabla} WHERE fecha = %s",
                (fecha,)
            )

            if cursor.fetchone() is None:
                cursor.execute(
                    f"""INSERT INTO {tabla}
                    (fecha, open_price, high, low, close_price, volume)
                    VALUES (%s, %s, %s, %s, %s, %s)""",
                    (
                        fecha,
                        str(registro.get("open", "")),
                        str(registro.get("high", "")),
                        str(registro.get("low", "")),
                        str(registro.get("close", "")),
                        str(registro.get("volume", ""))
                    )
                )
                insertados += 1

        logger.info(
            f"{tabla}: {insertados} insertados ({len(registros)} en archivo)"
        )

        total_insertados += insertados

    conexion.commit()
    logger.info(f"Yahoo: {total_insertados} nuevos registros")


def cargar_opensky(conexion):

    datos = leer_json("opensky")
    if not datos:
        return

    cursor = conexion.cursor()

    resumen = datos
    fecha = datos.get(
        "fecha_consulta", datetime.now().strftime("%Y-%m-%d")
    )

    cursor.execute(
        "SELECT 1 FROM raw.opensky_trafico WHERE fecha = %s",
        (fecha,)
    )

    if cursor.fetchone() is None:
        cursor.execute(
            """INSERT INTO raw.opensky_trafico
            (fecha, total_aviones, en_vuelo, en_tierra,
             velocidad_promedio, altitud_promedio, pais_mas_frecuente)
            VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (
                fecha,
                str(resumen.get("total_aviones", "")),
                str(resumen.get("en_vuelo", "")),
                str(resumen.get("en_tierra", "")),
                str(resumen.get("velocidad_promedio_kmh", "")),
                str(resumen.get("altitud_promedio_m", "")),
                str(resumen.get("pais_mas_frecuente", ""))
            )
        )
        logger.info("raw.opensky_trafico: 1 insertado")
    else:
        logger.info("raw.opensky_trafico: ya existe")

    conexion.commit()
    logger.info("OpenSky: carga completada")


def main():

    logger.info("=" * 60)
    logger.info("INICIO DE CARGA DE DATOS")
    logger.info("=" * 60)

    conexion = conectar_postgresql()

    try:
        logger.info("\n--- Banxico ---")
        cargar_banxico(conexion)

        logger.info("\n--- INEGI ---")
        cargar_inegi(conexion)

        logger.info("\n--- Yahoo ---")
        cargar_yahoo(conexion)

        logger.info("\n--- OpenSky ---")
        cargar_opensky(conexion)

        logger.info("=" * 60)
        logger.info("CARGA EXITOSA")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Error: {e}")
        conexion.rollback()
        raise

    finally:
        conexion.close()
        logger.info("Conexión cerrada")


if __name__ == "__main__":
    main()