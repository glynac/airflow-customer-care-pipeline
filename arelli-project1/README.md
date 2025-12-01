# Airflow Docker Environment

## Dataset Overview
This pipeline ingests customer care email records from a local CSV file, validates structure, applies cleaning transformations, and loads the data into a PostgreSQL target table for analytics.

## Dataset Purpose
Used for customer support analytics including:

Agent performance
Critical issue tracking
Sentiment & satisfaction monitoring
Email categorization and routing

### Source File Location
/opt/airflow/extraction/customer_care_emails/sample_data/train.csv

## Target Table (PostgreSQL)
Table name: customer_care_emails DDL file:
extraction/customer_care_emails/sample_data/config/create_table.sql
Schema contract reference:
extraction/customer_care_emails/sample_data/config/schema_expected.yaml

##  Required Environment Variables
Defined in .env.example and used by Docker + Airflow runtime: 
PG_HOST=airflow_postgres
PG_PORT=5432
PG_DB=airflow
PG_USER=airflow
PG_PASSWORD=airflow

## Running the Pipeline
1. Start services
From the arelli-project1 folder:
docker compose up -d
2. Open Airflow UI
http://localhost:8080
3. Trigger DAG
Locate customer_care_emails_ingest → Click Trigger DAG ( icon)

## DAG Overview
DAG file path:
dags/customer_care_emails_ingest.py

# Tasks & Dependencies
<img width="589" height="202" alt="image" src="https://github.com/user-attachments/assets/6acebbea-9fd1-4bf4-afda-c5d95925cb2d" />
# Task Flow
<img width="838" height="123" alt="image" src="https://github.com/user-attachments/assets/c86c35b9-dec8-413a-867f-ad8a698f12ee" />
#  Runbook (Operational Guide)
Updating schema or new fields
Modify schema YAML file
Update create_table.sql
Add transformation logic in Python
Clear and rerun DAG
## New CSV drops / incremental batches
Replace CSV inside sample_data
Ensure status != done logic handles previously loaded rows
Trigger DAG manually
# Checklist before dataset commits
<img width="404" height="247" alt="image" src="https://github.com/user-attachments/assets/ee8ba5cd-96c9-40c1-bb39-4594d0e53ec3" />
# Completion Criteria
This documentation ensures future engineers can: - Start the environment - Understand Airflow DAG flow -
Troubleshoot failures - Extend pipeline logic safely






