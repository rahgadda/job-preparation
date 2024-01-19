COPY jobs FROM '/workspace/knowledge-base/01-ML/03-projects/01-streamlit/01-DuckDB/hr.parquet/jobs.parquet' (FORMAT 'parquet');
COPY regions FROM '/workspace/knowledge-base/01-ML/03-projects/01-streamlit/01-DuckDB/hr.parquet/regions.parquet' (FORMAT 'parquet');
COPY countries FROM '/workspace/knowledge-base/01-ML/03-projects/01-streamlit/01-DuckDB/hr.parquet/countries.parquet' (FORMAT 'parquet');
COPY locations FROM '/workspace/knowledge-base/01-ML/03-projects/01-streamlit/01-DuckDB/hr.parquet/locations.parquet' (FORMAT 'parquet');
COPY departments FROM '/workspace/knowledge-base/01-ML/03-projects/01-streamlit/01-DuckDB/hr.parquet/departments.parquet' (FORMAT 'parquet');
COPY employees FROM '/workspace/knowledge-base/01-ML/03-projects/01-streamlit/01-DuckDB/hr.parquet/employees.parquet' (FORMAT 'parquet');
