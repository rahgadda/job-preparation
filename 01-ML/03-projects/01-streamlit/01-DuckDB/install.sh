#!/bin/bash

# Installing Duckdb
pip install duckdb

# Set the database file name
db_file="hr.db"

# Load data from .sql file
sql_file="oracle_hr.sql"

# Check if the SQL file exists
if [ -f $db_file ]; then
    echo "Loading data from $db_file"
    
    # Loading the DuckDB database from hr.db
    duckdb $db_file
else
    echo "Creating database $db_file"

    # Create the DuckDB database and loading sql file
    duckdb $db_file
    duckdb -f $sql_file
fi


