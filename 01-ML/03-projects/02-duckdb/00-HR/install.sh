#!/bin/bash

# Installing Duckdb
cd /workspace/knowledge-base/01-ML/03-projects/02-duckdb/00-HR
wget https://github.com/duckdb/duckdb/releases/download/v0.9.2/duckdb_cli-linux-amd64.zip
unzip duckdb_cli-linux-amd64.zip
rm -rf duckdb_cli-linux-amd64.zip

# Create Virutal Python Environment
sudo pip install virtualenv
python -m venv hr_venv
source hr_venv/bin/activate
cd hr_venv
source hr_venv/bin/deactivate

# Set the database file name
db_file="hr.db"

# Load data from .sql file
sql_file="oracle_hr.sql"

# Check if the SQL file exists
if [ -f $db_file ]; then
    echo "Loading data from $db_file"
    
    # Loading the DuckDB database from hr.db
    ./duckdb $db_file
else
    echo "Creating database $db_file"

    # Create the DuckDB database
    ./duckdb $db_file -c "INSTALL sqlite; LOAD sqlite; INSTALL httpfs;  LOAD httpfs; select * from duckdb_extensions(); SHOW tables;"
    # Load SQL to the database - Manual
    # Create PARQUET of database
    ./duckdb $db_file -c "EXPORT DATABASE '/workspace/knowledge-base/01-ML/03-projects/01-streamlit/01-DuckDB/hr.parquet' (FORMAT PARQUET);"
fi