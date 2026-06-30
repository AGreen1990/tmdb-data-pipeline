import os
import json

import requests
from dotenv import load_dotenv

print("1. Loading environment variables...")
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

print("2. Setting up URL...")
url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={API_KEY}"

print("3. Send request to TMDB...")
response =requests.get(url)

print(f"4. Result: {response.status_code}")

#---to show paylod

if response.status_code == 200:
    data = response.json()
 # --- Save the data to a local file   
    with open("raw_movies.json", "w") as file:
        json.dump(data, file, indent=4)

    print("Success! Data landed in raw_movies.json")

# Last updated: June 30th. Ready for Load phase.