import os
import csv
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

# Load the local .env file to securely access credentials
load_dotenv()

def load_data_to_neon():
    print("Connecting to Neon Database...")

    #1. Grab your connection string from the environment variables
    db_url = os.environ.get("DATABASE_URL")

    #2. Read the CSV that your script created in the Transform step
    df = pd.read_csv(transformed_movies.csv)

    #3. Establish a database connection
    engine = create_engine(db_url)

    #4 Write DataFrame directly to a SQL table named 'movies'
    df.to_sql("movies", con=engine, if_exists="replace", index=False)

    print("Succes: TMDB data safely into Neon!")

if __name__ == "__main__":
    load_data_to_neon()