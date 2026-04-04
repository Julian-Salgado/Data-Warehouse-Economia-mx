from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from airflow.operators.empty import EmptyOperator
import sys
import os
import subprocess

if os.path.exists("/opt/airflow/project"):
    PROYECTO_PATH = "/opt/airflow/project"
    WINDOWS_HOST = "postgres"
else:
    PROYECTO_PATH = "/mnt/c/Users/julii/Documents/data-warehouse-economia-mx"
    WINDOWS_HOST = "172.21.0.1"

DBT_PROJECT_PATH = f"{PROYECTO_PATH}/dbt_project"

default_args = {
    "owner": "julian",
    "depends_on_past": False,
    "start_date": datetime(2026, 4, 3),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def extraer_banxico():
    sys.path.insert(0, PROYECTO_PATH)
    os.chdir(PROYECTO_PATH)
    from src.extract.extract_banxico import extraer_banxico as ejecutar
    ejecutar()

def extraer_inegi():
    sys.path.insert(0, PROYECTO_PATH)
    os.chdir(PROYECTO_PATH)
    from src.extract.extract_inegi import extraer_inegi as ejecutar
    ejecutar()

def extraer_yahoo():
    sys.path.insert(0, PROYECTO_PATH)
    os.chdir(PROYECTO_PATH)
    from src.extract.extract_yahoo import extraer_yahoo as ejecutar
    ejecutar()

def extraer_opensky():
    sys.path.insert(0, PROYECTO_PATH)
    os.chdir(PROYECTO_PATH)
    from src.extract.extract_opensky import extraer_opensky as ejecutar
    ejecutar()

def cargar_datos_raw():
    sys.path.insert(0, PROYECTO_PATH)
    os.chdir(PROYECTO_PATH)
    os.environ["POSTGRES_HOST"] = WINDOWS_HOST
    from src.load.load_raw import main
    main()

def validar_calidad():
    os.chdir(PROYECTO_PATH)
    mi_env = os.environ.copy()
    mi_env["POSTGRES_HOST"] = WINDOWS_HOST

    resultado = subprocess.run(
        ["python3", f"{PROYECTO_PATH}/great_expectations/validate_data.py"],
        capture_output=True,
        text=True,
        env=mi_env,
        cwd=PROYECTO_PATH,
    )

    print(resultado.stdout)
    if resultado.returncode != 0:
        print(resultado.stderr)
        raise Exception("Validacion de calidad fallo")

def verificar_extracciones(**context):
    from datetime import date

    hoy = date.today().strftime("%Y%m%d")

    archivos_esperados = [
        f"{PROYECTO_PATH}/data/banxico_{hoy}.json",
        f"{PROYECTO_PATH}/data/inegi_{hoy}.json",
        f"{PROYECTO_PATH}/data/yahoo_{hoy}.json",
        f"{PROYECTO_PATH}/data/opensky_{hoy}.json",
    ]

    archivos_faltantes = []
    for archivo in archivos_esperados:
        if not os.path.exists(archivo):
            archivos_faltantes.append(archivo)

    if archivos_faltantes:
        print(f"ARCHIVOS FALTANTES: {archivos_faltantes}")
        return "alerta_extraccion_fallida"
    else:
        print("Todas las extracciones exitosas")
        return "cargar_datos_raw"

def alerta_fallo_extraccion():
    print("=" * 60)
    print("ALERTA: Una o mas extracciones fallaron")
    print("Revisa los logs de cada tarea de extraccion")
    print("=" * 60)

def alerta_exito_pipeline():
    print("=" * 60)
    print("EXITO: Pipeline completo ejecutado correctamente")
    print(f"Fecha: {datetime.now()}")
    print("Datos extraidos, cargados, validados y transformados")
    print("=" * 60)

with DAG(
    dag_id="dag_data_warehouse_economia",
    default_args=default_args,
    description="Pipeline completo del data warehouse de economia mexicana",
    schedule="0 6 * * *",
    catchup=False,
    tags=["data_warehouse", "economia", "mexico"],
) as dag:

    inicio = EmptyOperator(task_id="inicio")

    with TaskGroup(group_id="extraer_datos") as grupo_extraccion:
        t_banxico = PythonOperator(
            task_id="extraer_banxico",
            python_callable=extraer_banxico,
        )
        t_inegi = PythonOperator(
            task_id="extraer_inegi",
            python_callable=extraer_inegi,
        )
        t_yahoo = PythonOperator(
            task_id="extraer_yahoo",
            python_callable=extraer_yahoo,
        )
        t_opensky = PythonOperator(
            task_id="extraer_opensky",
            python_callable=extraer_opensky,
        )

    t_verificar = BranchPythonOperator(
        task_id="verificar_extracciones",
        python_callable=verificar_extracciones,
    )

    t_alerta_extraccion = PythonOperator(
        task_id="alerta_extraccion_fallida",
        python_callable=alerta_fallo_extraccion,
    )

    t_cargar = PythonOperator(
        task_id="cargar_datos_raw",
        python_callable=cargar_datos_raw,
    )

    t_validar = PythonOperator(
        task_id="validar_calidad",
        python_callable=validar_calidad,
    )

    t_dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"cd {DBT_PROJECT_PATH} && dbt run",
    )

    t_dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"cd {DBT_PROJECT_PATH} && dbt test",
    )

    t_exito = PythonOperator(
        task_id="alerta_exito",
        python_callable=alerta_exito_pipeline,
    )

    inicio >> grupo_extraccion
    grupo_extraccion >> t_verificar
    t_verificar >> t_alerta_extraccion
    t_verificar >> t_cargar >> t_dbt_run >> t_dbt_test >> t_validar >> t_exito