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
