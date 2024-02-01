# Kestra.io

## Overview
- Kestra is a universal open-source orchestrator that makes both scheduled and event-driven workflows easy.
- Building blocks
  - `Flows:`
    - Defined declartively to keep the orchestration code portable and language-agnostic. 
    - Defined in yaml.
    - It has three parts
      - **Mandatory:**
        - `id:` Name of the flow. Should be unique within a namespace.
        - `namespace:` Used to isolate environments like dev, prod.
        - `tasks:` 
          - Atomic actions in flow.
          - Tasks that will be executed in the order they are defined.
          - Tasks are defined in the form of a list.
          - By default, all tasks in the list will be executed sequentially
          - Tasks can also be customized to execute in parallel. These are called `Flowable` tasks.
          - Task also have parameters. Each task will have additional parameters depend on task type
            - `id:` Unique identification of the task in task list.
            - `type:`
              - `Core:` 
                - Available in `io.kestra.core.tasks.flows`.
                - Used to declare which processes should run in parallel or sequentially or conditional branching, iterating over a list of items, pausing or allowing certain tasks to fail without failing the execution.
              - `Scripts:`
                - Used to run scripts in Docker containers or local processes.
                - These include Python, Node.js, R, Julia, Shell or PowerShell.
              - `Internal Storage:`
                - Available in `io.kestra.core.tasks.storages`.
                - These along with output are used to interact with internal storage.
                - Kestra uses internal storage to pass data between tasks. It is mainly used to pass data within a single flow execution.
              - `State Store:`
                - If you need to pass data between different flow executions, you can use the State Store.
                - The tasks Set, Get and Delete from the io.kestra.core.tasks.states category allow you to persist files between executions (even across namespaces).
      - **Optional:**
        - `labels:` Another layer of organization, allowing you to group flows using key-value pairs.
        - `description:` Enhace flow documentation. Supports markdown syntax.
  - `Inputs:`
    - Used to declare variabels instead of hardcoding.
    - Inputs can be accessed in any task using expression `{{ inputs.input_name }}`.
    - It contains below
      - **Mandatory:**
        - `name:` Variable name.
        - `type:` Data type of varaiables. Supports STRING, INT - No decimal points, BOOLEAN - true or false. 
      - **Optional**
        - `defaults:` Default value of input varaible to be considered if not provided.
        ```yaml
        inputs:
        - name: user
          type: STRING
          defaults: Rick Astley
        ```

## History

## Installation
- Below are steps to load parquet data transform using DBT and persist into Snowflake
  ```bash
  # Installation
  cd 01-ML/03-projects/Kestra-io
  curl -o docker-compose.yml https://raw.githubusercontent.com/kestra-io/kestra/develop/docker-compose.yml
  docker compose up
  # Deployment URL: 
  # http://localhost:8080/ui/welcome
  
  # Creating duckdb with parquet files, transform with dbt and persist to snowflake
  # Navigate to Flows -> Create -> 03-projects/Kestra-io/demo.yaml -> Execute 
  ```
## Modules


## Tutorial
- [Docs](https://kestra.io/docs)
- [Plugins](https://kestra.io/plugins)
- [Demo](https://us.kestra.cloud/ui/login?from=/ui/demo/dashboard)
- [Data Ingestion, Transformation and Orchestration](https://dev.to/kestra/end-to-end-data-ingestion-transformation-and-orchestration-with-airbyte-dbt-and-kestra-1lmo)

## Reference
- [Airbyte - Connector based data replicator](https://airbyte.com/)