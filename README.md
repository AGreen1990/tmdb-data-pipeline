# TMDB Data Engineering Pipeline

This repository contains an automated end-to-end Data Engineering ETL pipeline extracting trending movie data from the TMDB API. The data is processed via Python and loaded into a Neon Serverless PostgreSQL database, with orchestration handled entirely by GitHub Actions CI/CD workflows.

## Data Architecture (Medallion Concept)

The project follows a modular Extract, Transform, and Load (ETL) design, mapped conceptually to a Medallion Architecture:

*   **Bronze Layer (Raw):** `extract.py` handles paginated REST API requests to the TMDB API, safely managing rate limits and persisting the raw, nested JSON payloads locally (`raw_movies.json`).
*   **Silver Layer (Structured):** `transform.py` parses the raw JSON, flattens nested dictionaries, filters necessary fields, and outputs a clean, row-level CSV (`transformed_movies.csv`).
*   **Gold Layer (Serving):** `load.py` connects to Neon Serverless PostgreSQL and upserts the structured records into target relational tables, ready for downstream SQL analytics.

## Repository Structure

```text
tmdb-data-pipeline/
├── .github/
│   └── workflows/
├── extract.py
├── transform.py
├── load.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Tech Stack

- Language: Python 3.9+ (requests, json, csv, psycopg2)
- Database: Neon Serverless PostgresSQL
- Orchestration: GitHub Actions CI/CD
- Version Control: Git & Github

Local Setup & Execution
To run this pipeline locally, you will need Python 3.9+ installed on your machine. 

1. Clone the repository

Bash
git clone [https://github.com/AGreen1990/tmdb-data-pipeline.git](https://github.com/AGreen1990/tmdb-data-pipeline.git)
cd tmdb-data-pipeline

2. Configure Virtual Machine

Bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Environment Variables
- This project requires API keys and database credentials to function. Create a .env file in the root directory:

Bash
touch .env

- Add the following variables to your .env file, replacing the placeholder values with your actual credentials:

TMDB_API_KEY="your_tmdb_v3_api_key_here"
NEON_DB_CONNECTION_STRING="postgresql://user:password@endpoint.neon.tech/dbname"

4. Execute the Pipeline
- Run the pipeline sequentially to extract the data, transform it into a structured CSV, and load it into your Neon PostgreSQL database:

Bash
# 1. Fetch raw JSON data from TMDB API (Bronze)
python3 extract.py

# 2. Flatten JSON and prepare CSV (Silver)
python3 transform.py

# 3. Upsert records into Neon PostgreSQL (Gold)
python3 load.py
