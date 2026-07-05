import os
import csv
import snowflake.connector
from dotenv import load_dotenv

# Load the local .env file to securely access credentials
load_dotenv()

def load_data_to_snowflake():
    #1 establish the connection to snowflake
    print("Connecting to Snowflake...")
    conn = snowflake.connector.connect(
        user=os.getenv("SF_USER"),
        password=os.getenv("SF_PASSWORD"),
        account=os.getenv("SF_ACCOUNT"),
        warehouse="COMPUTE_WH",
        database="TMDB_PROJECT_DB",
        schema="RAW DATA",
        role="ACCOUNTADMIN"
    )

    #A cursor is like a tunnel that lets us send SQL commands to a database
    cursor = conn.cursor()

    try:
        # 2. Prevent Duplicates: Truncate the table
        print("Truncating the existing Movies table. . .")
        cursor.execute("TRUNCATE TABLE TMDB_PROJECT_DB.RAW_DATA.MOVIES")

        # 3. Read the fresh data from local CSV
        movies_dict = {}
        with open("transformed_movies.csv", "r", encoding="utf-8") as file:
            csv_reader = csv.reader(file)
            next(csv_reader) # Crucial: Skip the header row!

            #loop through the CSV and package the rows into a list
            for row in csv_reader:
                cleaned_row = [None if val == "" else val for val in row]
                
                movies_id = cleaned_row[0]
                #Storing in dictionary with movie_id as the Key guarantees uniqueness
                # if duplicate id comes through, it overwrites the old one
                movies_dict[movies_id] = tuple(cleaned_row)
        #Converts the dictionary values back into a list so Snowflake can read it
        movies_data = list(movies_dict.values()) 


        
        #4. Insert the new data
        print(f"Inserting {len(movies_data)} fresh rows into Snowflake...")
        insert_query = """
        INSERT INTO TMDB_PROJECT_DB.RAW_DATA.MOVIES
        (movie_id, title, release_date, popularity, vote_average, primary_genre)
        VALUES(%s, %s, %s, %s, %s, %s)
        """

        #executemany takes the query and applies it to every row in the list instantly
        cursor.executemany(insert_query, movies_data)

        print("✅ Success! Pipeline complete. Data is live in Snowflake.")

    finally:
        #5. Always close the connection so we don't waste Snowflake compute credits
        cursor.close()
        conn.close()

if __name__ == "__main__":
    load_data_to_snowflake()