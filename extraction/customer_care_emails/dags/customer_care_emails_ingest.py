import os
import pandas as pd
import yaml
import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

DATASET_NAME = "customer_care_emails"

# Correct base paths inside container
BASE_PATH = f"/opt/airflow/extraction/{DATASET_NAME}"
CSV_PATH = f"{BASE_PATH}/sample_data/train.csv"
CLEANED_PATH = f"{BASE_PATH}/sample_data/cleaned.csv"
SCHEMA_PATH = f"{BASE_PATH}/sample_data/config/schema_expected.yaml"
DDL_PATH = f"{BASE_PATH}/sample_data/config/create_table.sql"

# Load env variables from docker compose
PG_HOST = os.getenv("PG_HOST", "postgres")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DB = os.getenv("PG_DB", "airflow")
PG_USER = os.getenv("PG_USER", "airflow")
PG_PASSWORD = os.getenv("PG_PASSWORD", "airflow")


def check_file():
    """Check if CSV file exists."""
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")
    print("CSV exists:", CSV_PATH)


def validate_schema():
    """Validate CSV schema using YAML file."""
    df = pd.read_csv(CSV_PATH)

    with open(SCHEMA_PATH, "r") as f:
        schema = yaml.safe_load(f)

    expected_cols = [col["name"] for col in schema["columns"]]
    actual_cols = list(df.columns)

    print("EXPECTED:", expected_cols)
    print("ACTUAL:", actual_cols)

    if expected_cols != actual_cols:
        raise ValueError(f"Schema mismatch!\nExpected: {expected_cols}\nActual: {actual_cols}")

    print("Schema validation passed!")


def transform_data():
    """Clean and normalize CSV data."""
    df = pd.read_csv(CSV_PATH)

    # Remove whitespace in headers
    df.columns = [col.strip() for col in df.columns]

    # Clean values per column
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip().replace("nan", None)

    df.to_csv(CLEANED_PATH, index=False)
    print(f"Cleaned file saved to {CLEANED_PATH}")


def load_to_postgres():
    """Insert cleaned data into target PostgreSQL table."""
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT, database=PG_DB, user=PG_USER, password=PG_PASSWORD
    )
    cur = conn.cursor()

    # Create table
    with open(DDL_PATH, "r") as ddl:
        cur.execute(ddl.read())
        conn.commit()

    df = pd.read_csv(CLEANED_PATH)

    for _, row in df.iterrows():
        cols = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(row))
        query = f"INSERT INTO customer_care_emails ({cols}) VALUES ({placeholders})"
        cur.execute(query, tuple(row.values))

    conn.commit()
    cur.close()
    conn.close()
    print("Data loaded into PostgreSQL successfully!")


with DAG(
    dag_id="customer_care_emails_ingest",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["customer_care_emails"],
) as dag:

    task_check_file = PythonOperator(
        task_id="check_file",
        python_callable=check_file,
    )

    task_validate = PythonOperator(
        task_id="validate_schema",
        python_callable=validate_schema,
    )

    task_transform = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
    )

    task_load = PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_to_postgres,
    )

    task_check_file >> task_validate >> task_transform >> task_load