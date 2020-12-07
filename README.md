# airflow-sql-tutorial
This repo contains an Astronomer project with multiple example DAGs showing how to use Airflow for SQL use cases. A guide discussing the DAGs and concepts in depth will be published soon.

## Tutorial Overview
This tutorial has five DAGs showing how to accomplish the following SQL use cases:

 - Executing two dependent queries
 - Executing a paramterized query
 - Loading data into a database
 - Executing an ETL pipeline with transformations in Pandas
 - Executing a query using [dag-factory](https://github.com/ajbosco/dag-factory)


## Getting Started
The easiest way to run these example DAGs is to use the Astronomer CLI to get an Airflow instance up and running locally:

 1. [Install the Astronomer CLI](https://www.astronomer.io/docs/cloud/stable/develop/cli-quickstart)
 2. Clone this repo somewhere locally and navigate to it in your terminal
 3. Initialize an Astronomer project by running `astro dev init`
 4. Start Airflow locally by running `astro dev start`
 5. Navigate to localhost:8080 in your browser and you should see the tutorial DAGs there
