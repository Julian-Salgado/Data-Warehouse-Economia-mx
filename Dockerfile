FROM apache/airflow:2.10.5-python3.12

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

COPY requirements.txt /opt/airflow/requirements.txt

RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

COPY --chown=airflow:root src/ /opt/airflow/project/src/
COPY --chown=airflow:root great_expectations/ /opt/airflow/project/great_expectations/
COPY --chown=airflow:root dbt_project/ /opt/airflow/project/dbt_project/
COPY --chown=airflow:root data/ /opt/airflow/project/data/
COPY --chown=airflow:root .env /opt/airflow/project/.env

COPY --chown=airflow:root airflow/dags/ /opt/airflow/dags/