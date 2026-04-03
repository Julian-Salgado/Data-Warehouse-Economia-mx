import sys
import traceback
import great_expectations as gx
from great_expectations.expectations import (
    ExpectColumnValuesToBeBetween,
    ExpectColumnValuesToNotBeNull,
    ExpectColumnValuesToBeUnique,
    ExpectTableRowCountToBeBetween,
)
from dotenv import load_dotenv
import os

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "12345")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "data_warehouse_economia")

CONNECTION_STRING = (
    f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)


def ejecutar_validacion(nombre_tabla, schema, tabla, expectativas):

    context = gx.get_context(mode="ephemeral")

    datasource = context.data_sources.add_postgres(
        name=f"ds_{nombre_tabla}",
        connection_string=CONNECTION_STRING,
    )

    asset = datasource.add_table_asset(
        name=nombre_tabla,
        schema_name=schema,
        table_name=tabla,
    )

    batch_def = asset.add_batch_definition_whole_table(
        name=f"batch_{nombre_tabla}"
    )

    suite = context.suites.add(
        gx.ExpectationSuite(name=f"suite_{nombre_tabla}")
    )
    for exp in expectativas:
        suite.add_expectation(exp)

    validation = context.validation_definitions.add(
        gx.ValidationDefinition(
            name=f"val_{nombre_tabla}",
            data=batch_def,
            suite=suite,
        )
    )

    resultado = validation.run()

    for res in resultado.results:
        nombre = res.expectation_config.type
        exito = res.success

        if exito:
            print(f"    [PASS] {nombre}")
        else:
            print(f"    [FAIL] {nombre}")
            result_dict = res.result
            if "unexpected_count" in result_dict:
                print(
                    f"           Valores inesperados: {result_dict['unexpected_count']}"
                )
            if "observed_value" in result_dict:
                print(
                    f"           Valor observado: {result_dict['observed_value']}"
                )

    return resultado.success


def main():
    print("=" * 60)
    print("  GREAT EXPECTATIONS — Validacion de calidad de datos")
    print("  Data Warehouse de Economia Mexicana")
    print("=" * 60)

    resultados = {}

    # FACT_INDICADORES
    print("\n" + "=" * 60)
    print("  VALIDANDO: fact_indicadores_economicos")
    print("=" * 60)

    try:
        resultados["fact_indicadores_economicos"] = ejecutar_validacion(
            nombre_tabla="fact_indicadores",
            schema="marts",
            tabla="fact_indicadores_economicos",
            expectativas=[
                ExpectTableRowCountToBeBetween(min_value=1),
                ExpectColumnValuesToNotBeNull(column="valor"),
                ExpectColumnValuesToNotBeNull(column="fecha"),
                ExpectColumnValuesToNotBeNull(column="indicador_id"),
                ExpectColumnValuesToBeUnique(column="id"),
            ],
        )
    except Exception as e:
        print(f"    [ERROR] {e}")
        resultados["fact_indicadores_economicos"] = False

    # FACT_TRAFICO
    print("\n" + "=" * 60)
    print("  VALIDANDO: fact_trafico_aereo")
    print("=" * 60)

    try:
        resultados["fact_trafico_aereo"] = ejecutar_validacion(
            nombre_tabla="fact_trafico",
            schema="marts",
            tabla="fact_trafico_aereo",
            expectativas=[
                ExpectTableRowCountToBeBetween(min_value=1),
                ExpectColumnValuesToNotBeNull(column="total_aviones"),
                ExpectColumnValuesToBeBetween(
                    column="total_aviones", min_value=1
                ),
                ExpectColumnValuesToBeBetween(
                    column="velocidad_promedio",
                    min_value=0,
                    max_value=1200,
                ),
                ExpectColumnValuesToBeUnique(column="id"),
            ],
        )
    except Exception as e:
        print(f"    [ERROR] {e}")
        resultados["fact_trafico_aereo"] = False

    # DIM_FECHA
    print("\n" + "=" * 60)
    print("  VALIDANDO: dim_fecha")
    print("=" * 60)

    try:
        resultados["dim_fecha"] = ejecutar_validacion(
            nombre_tabla="dim_fecha",
            schema="marts",
            tabla="dim_fecha",
            expectativas=[
                ExpectTableRowCountToBeBetween(min_value=1),
                ExpectColumnValuesToBeUnique(column="fecha"),
                ExpectColumnValuesToNotBeNull(column="fecha"),
            ],
        )
    except Exception as e:
        print(f"    [ERROR] {e}")
        resultados["dim_fecha"] = False

    # DIM_INDICADOR
    print("\n" + "=" * 60)
    print("  VALIDANDO: dim_indicador")
    print("=" * 60)

    try:
        resultados["dim_indicador"] = ejecutar_validacion(
            nombre_tabla="dim_indicador",
            schema="marts",
            tabla="dim_indicador",
            expectativas=[
                ExpectTableRowCountToBeBetween(min_value=1),
                ExpectColumnValuesToBeUnique(column="indicador_id"),
                ExpectColumnValuesToNotBeNull(column="indicador_id"),
                ExpectColumnValuesToNotBeNull(column="nombre"),
            ],
        )
    except Exception as e:
        print(f"    [ERROR] {e}")
        resultados["dim_indicador"] = False

    # DIM_FUENTE
    print("\n" + "=" * 60)
    print("  VALIDANDO: dim_fuente")
    print("=" * 60)

    try:
        resultados["dim_fuente"] = ejecutar_validacion(
            nombre_tabla="dim_fuente",
            schema="marts",
            tabla="dim_fuente",
            expectativas=[
                ExpectTableRowCountToBeBetween(min_value=1),
                ExpectColumnValuesToBeUnique(column="fuente_id"),
                ExpectColumnValuesToNotBeNull(column="fuente_id"),
                ExpectColumnValuesToNotBeNull(column="nombre"),
            ],
        )
    except Exception as e:
        print(f"    [ERROR] {e}")
        resultados["dim_fuente"] = False

    # RESUMEN
    print("\n" + "=" * 60)
    print("  RESUMEN FINAL")
    print("=" * 60)

    todo_ok = True
    for tabla_nombre, paso in resultados.items():
        estado = "PASS" if paso else "FAIL"
        print(f"  {estado} — {tabla_nombre}")
        if not paso:
            todo_ok = False

    total = len(resultados)
    pasaron = sum(1 for v in resultados.values() if v)

    if todo_ok:
        print(f"\n  >>> TODAS LAS VALIDACIONES PASARON ({pasaron}/{total}) <<<")
    else:
        print(f"\n  >>> ALGUNAS VALIDACIONES FALLARON ({pasaron}/{total}) <<<")

    print("=" * 60)
    return 0 if todo_ok else 1


if __name__ == "__main__":
    codigo_salida = main()
    sys.exit(codigo_salida)