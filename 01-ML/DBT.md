# Data Build Tool - DBT 

## Overview
- It is becomming a standard SQL tempalting process for Data Transformation in [ETL/ELT - Extract, Load, Transform] data pipelines.
  - `ETL:`
    - Used to extract data from different OLTP environment.
    - Transform the data to based on the destination format provided in OLAP environment.
    - Load the data into OLAP/Data Warehouse.
    - This centralized data was later used for Analytics, AI/ML or Down Stream Processing. 
    - Used by on-premise dataware house tools like infomatica etc...
    ![](00-images/ETL.png)
  - `ELT:`
    - Data from different OLTP environment is directly loaded into OLAP environment.
    - Transformation is then perfomed using elastic compute.
    - Used by cloud providers like Snowflake, Databricks etc...
    ![](00-images/ELT.png)
- It is an open-source command line tool that helps analysts and engineers transform data in their warehouse more effectively.
- It enables analytics engineers to transform data in their warehouses by writing select statements, and turns these select statements into tables and views.
- dbt code is a combination of `SQL` and `Jinja` - a common templating language.
- At the most basic level, dbt has two components: 
  - `Compiler`: Converts code into Raw SQL
  - `Runner`: Executes inside a datawarehouse
- It works on below principles
  ![](00-images/dt_overview.png)
  ![](00-images/dbt-how-it-works.png)

## History
- It was founded by Fishtown Analytics (later named as dbt Labs) in 2016.
- In 2018, the dbt Labs team released a commercial product on top of dbt Core.
- In Feb 2022 they received $222 million with a valuation of $4.2 Billion.

## Modules
- `Naming Convention:`
  - `Sources (src):` Refer to the raw table data that have been built in the warehouse through a loading process. (We will cover configuring Sources in the Sources module)
  - `Staging (stg):` refers to models that are built directly on top of sources. These have a one-to-one relationship with sources tables. These are used for very light transformations that shape the data into what you want it to be. These models are used to clean and standardize the data before transforming data downstream. Note: These are typically materialized as views.
  - `Intermediate (int):` refers to any models that exist between final fact and dimension tables. These should be built on staging models rather than directly on sources to leverage the data cleaning that was done in staging.
  - `Fact (fct):` refers to any data that represents something that occurred or is occurring. Examples include sessions, transactions, orders, stories, votes. These are typically skinny, long tables.
  - `Dimension (dim):` refers to data that represents a person, place or thing. Examples include customers, products, candidates, buildings, employees.
  ![](00-images/dbt_naming.png)

- `Model:`
  - These are SQL statements with extenssion `.sql`.
  - Each represent one modular peice of logic that will take raw data and build final transform data.
  - Mostly each has on-to-one relationship with table or view in data warehouse. 
  - dbt will create DDL/DML automatically.
  - `Config` block can be used to decalre result DDL is table or view. By default views are created.
    ```
    {{ config(
        materialized='table'
    ) }}
    ```
  - These are available in `models` folder.
  - `ref` functions are used to reference one model in another `{{ ref('stg_customers')}}`. These will be converted to actual tables during compilation.
- `Commands:` [Available here](https://docs.getdbt.com/reference/commands/build)
  

## Tutorial
- [Offical Documentation](https://docs.getdbt.com/)
- [Offical Courses](https://courses.getdbt.com/collections/courses)
- [Youtube - Playlist](https://www.youtube.com/playlist?list=PLohMhitTY9xuEVMpLG3xXhsKG9j2XCTeF)

## Refernce
- [Official Site](https://www.getdbt.com/)