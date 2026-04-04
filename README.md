<div align="center">

# Data Warehouse — Economia Mexicana

**Pipeline ELT end-to-end para indicadores economicos de Mexico**

Extraccion automatizada de 4 APIs · Modelo dimensional en PostgreSQL · Orquestacion con Airflow · Validacion con Great Expectations · Dashboard en Superset · Despliegue con Docker Compose

<br>

<img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/Apache%20Airflow-2.10.5-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white"/>
<img src="https://img.shields.io/badge/dbt-1.11.7-FF694B?style=for-the-badge&logo=dbt&logoColor=white"/>
<img src="https://img.shields.io/badge/Apache%20Superset-latest-20A6C9?style=for-the-badge&logo=apache&logoColor=white"/>
<img src="https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white"/>
<img src="https://img.shields.io/badge/Great%20Expectations-1.15-FF6F00?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white"/>

<br><br>

<img src="screenshots/dashboard_superset.png" alt="Dashboard" width="90%"/>

</div>

---

## Descripcion

Sistema de datos que centraliza 8 indicadores economicos de Mexico desde 4 fuentes (Banxico, INEGI, Yahoo Finance, OpenSky) en un data warehouse con modelo dimensional star schema. El pipeline ELT esta completamente orquestado, validado y containerizado.

| Metrica | Valor |
|---------|-------|
| Fuentes de datos | 4 APIs (Banxico, INEGI, Yahoo Finance, OpenSky) |
| Indicadores | 8 (tipo de cambio, TIIE, inflacion, IGAE, desempleo, petroleo, bolsa, oro) |
| Modelos dbt | 17 (9 staging, 3 intermediate, 5 marts) |
| Validaciones | 21 expectativas automaticas sobre 5 tablas |
| Tareas del DAG | 12 (con Task Groups, BranchOperator y alertas) |
| Servicios Docker | 4 (PostgreSQL, Airflow Webserver, Airflow Scheduler, Superset) |

---

## Arquitectura

```
  Banxico API ──┐
  INEGI API ────┤    ┌────────────┐    ┌────────────┐    ┌─────────────────┐    ┌────────────┐    ┌───────────┐
  Yahoo Fin. ───┼──▶ │ Extraccion │──▶ │ PostgreSQL │──▶ │ dbt (3 capas)   │──▶ │ Validacion │──▶ │ Superset  │
  OpenSky ──────┘    │ (Python)   │    │ (raw)      │    │ stg/int/marts   │    │ (GE)       │    │ Dashboard │
                     └────────────┘    └────────────┘    └─────────────────┘    └────────────┘    └───────────┘

                     └───────────────────── Apache Airflow (orquestacion) ──────────────────────┘
                     └───────────────────── Docker Compose (infraestructura) ───────────────────┘
```

---

## Modelo dimensional

Star schema con 3 dimensiones y 2 tablas de hechos:

```
    dim_fecha                 fact_indicadores_economicos              dim_indicador
  ┌──────────────┐          ┌──────────────────────────┐          ┌──────────────────┐
  │ fecha (PK)   │          │ id (PK)                  │          │ indicador_id (PK)│
  │ anio         │◀────────▶│ fecha (FK)               │◀────────▶│ nombre           │
  │ mes, dia     │          │ indicador_id (FK)        │          │ descripcion      │
  │ trimestre    │          │ fuente_id (FK)           │          │ unidad           │
  │ dia_semana   │          │ valor                    │          │ frecuencia       │
  │ es_festivo   │          │ valor_anterior           │          └──────────────────┘
  └──────────────┘          │ variacion_porcentual     │
                            │ promedio_movil_7d        │          dim_fuente
                            │ promedio_movil_30d       │        ┌──────────────────┐
                            └──────────────────────────┘        │ fuente_id (PK)   │
                                       ▲                        │ nombre           │
                                       └───────────────────────▶│ url_api          │
                                                                └──────────────────┘
```

| Fuente | Indicadores | Frecuencia |
|--------|-------------|------------|
| **Banxico** | Tipo de cambio USD/MXN, Tasa TIIE, Inflacion INPC | Diaria / Mensual |
| **INEGI** | IGAE (Actividad Economica), Desempleo | Mensual / Trimestral |
| **Yahoo Finance** | Petroleo WTI, IPC Bolsa Mexicana, Oro | Diaria |
| **OpenSky** | Trafico aereo sobre Mexico | Tiempo real |

---

## Quick start

> **Requisito:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo.

```bash
git clone https://github.com/tu-usuario/data-warehouse-economia-mx.git
cd data-warehouse-economia-mx

cp .env.example .env          # Configurar tokens de Banxico e INEGI
docker compose up --build     # Levantar todo el sistema (~2 min)
```

| Servicio | URL | Credenciales |
|----------|-----|--------------|
| Airflow | `http://localhost:8080` | admin / admin |
| Superset | `http://localhost:8088` | admin / admin1 |
| PostgreSQL | `localhost:5433` | postgres / 12345 |

Activar y ejecutar el DAG `dag_data_warehouse_economia` desde Airflow. El pipeline corre automaticamente en ~3 minutos.

```bash
docker compose down           # Apagar todos los servicios
```

---

## Screenshots

<table>
<tr>
<td width="50%">

**Dashboard — Superset**
<img src="screenshots/dashboard_superset.png" width="100%"/>

</td>
<td width="50%">

**Pipeline ejecutado — Airflow**
<img src="screenshots/airflow_dag_verde.png" width="100%"/>

</td>
</tr>
<tr>
<td width="50%">

**Grafo del DAG**
<img src="screenshots/airflow_dag_grafo.png" width="100%"/>

</td>
<td width="50%">

**Datos en PostgreSQL**
<img src="screenshots/datos_postgresql.png" width="100%"/>

</td>
</tr>
<tr>
<td colspan="2">
<div align="center">

**Servicios Docker Compose**

<img src="screenshots/docker_compose_ps.png" width="80%"/>
</div>
</td>
</tr>
</table>

---

## Stack

| Capa | Tecnologia | Implementacion |
|------|------------|----------------|
| **Extraccion** | Python, Requests, yfinance | 4 scripts con logging, manejo de errores y reintentos |
| **Almacenamiento** | PostgreSQL 16 | 4 esquemas (raw → staging → intermediate → marts) |
| **Transformacion** | dbt 1.11.7 | 17 modelos SQL, window functions, promedios moviles |
| **Validacion** | Great Expectations 1.15 | 21 expectativas programaticas con `EphemeralDataContext` |
| **Orquestacion** | Apache Airflow 2.10.5 | Task Groups, `BranchPythonOperator`, alertas de fallo/exito |
| **Visualizacion** | Apache Superset | 6 charts (lineas, tabla resumen) en dashboard interactivo |
| **Infraestructura** | Docker Compose | Multi-container con healthchecks y volumenes persistentes |

---

## Estructura

```
data-warehouse-economia-mx/
├── src/
│   ├── extract/                    # 4 scripts de extraccion (1 por API)
│   ├── load/
│   │   └── load_raw.py             # Carga a esquema raw
│   └── utils/
│       └── helpers.py              # Logging, env vars, JSON
│
├── dbt_project/models/
│   ├── staging/                    # 9 modelos — limpieza y tipado
│   ├── intermediate/               # 3 modelos — union y metricas derivadas
│   └── marts/                      # 5 modelos — star schema final
│
├── great_expectations/
│   └── validate_data.py            # 21 validaciones sobre marts
│
├── airflow/dags/
│   └── dag_data_warehouse.py       # DAG con deteccion automatica de entorno
│
├── init-sql/                       # DDL de esquemas y tablas raw
├── Dockerfile                      # Imagen base Airflow + dependencias
├── docker-compose.yml              # PostgreSQL + Airflow + Superset
├── requirements.txt
└── .env.example
```

---

## Decisiones tecnicas

| Problema | Solucion |
|----------|----------|
| INEGI migro su API de BIE a BISE (dic. 2025), rompiendo endpoints documentados | Adaptacion a nuevos endpoints; cobertura de INPC via Banxico como fallback |
| Great Expectations 1.x falla silenciosamente al reusar `EphemeralDataContext` | Contexto aislado por tabla, evitando contaminacion de estado |
| Conflicto de namespace entre directorio `great_expectations/` y el paquete pip | Ejecucion de validaciones via `subprocess` para aislar imports |
| Airflow no soporta Windows nativamente | DAG con deteccion automatica de entorno (WSL vs Docker) y ajuste dinamico de rutas |
| Tablas de marts no existen al primer arranque en Docker | Reordenamiento de dependencias en el DAG: dbt se ejecuta antes de la validacion |

---

## Roadmap

- [ ] Carga incremental (actualmente full refresh)
- [ ] Alertas por Slack/email ante fallos del pipeline
- [ ] Fuentes adicionales: remesas, balanza comercial, PIB
- [ ] CI/CD con GitHub Actions
- [ ] Graficas de correlacion entre indicadores en Superset

---

## Autor

**Julian Flores Salgado**
Ingeniero en Sistemas Computacionales — Tecnológico Nacional de México

<div align="center">

⭐ Si este proyecto te resultó interesante, no dudes en dejar una estrella.

</div>
