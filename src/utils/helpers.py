import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def obtener_variable(nombre):

    valor = os.getenv(nombre)
    if valor is None:
        raise ValueError(
            f"Variable '{nombre}' no encontrada. "
            f"Verifica que exista en el archivo .env"
        )
    return valor

def guardar_json(datos, nombre_fuente):

    fecha_hoy = datetime.now().strftime("%Y%m%d")
    nombre_archivo = f"{nombre_fuente}_{fecha_hoy}.json"
    ruta = os.path.join("data", nombre_archivo)

    os.makedirs("data", exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

    logging.info(f"Datos guardados en {ruta}")
    return ruta

def configurar_logging(nombre_fuente):
    
    os.makedirs("logs", exist_ok=True)

    fecha_hoy = datetime.now().strftime("%Y%m%d")
    archivo_log = os.path.join("logs", f"{nombre_fuente}_{fecha_hoy}.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(archivo_log, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )