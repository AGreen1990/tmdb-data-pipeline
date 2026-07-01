import os
import time
import json
import requests
from dotenv import load_dotenv

print("1. Loading environment variables...")
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

print("2. Fetching multiple pages from TMDB...")
all_movies = []
pages_to_fetch = 25

for page in range(1, pages_to_fetch + 1):
    #Note: the new &page={page} parameter at the end of the url from v1
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={API_KEY}&page={page}"
    response =requests.get(url)

    if response.status_code == 200:
        data = response.json()
 # .extend() adds the 20 movies from this page to our master list
        all_movies.extend(data["results"])
        print(f"Successfully fetched page {page}")
    else:
        print(f"Error on page {page}: {response.status_code}")

#Pausing for 0.2 second between requests to prevent blocking due to spamming
    time.sleep(0.2)

print("3. Saving combined data. . .")
#Wrapping the giant list back into a "results" dict
final_data = {"results": all_movies}

with open("raw_movies.json", "w") as file:
        json.dump(final_data, file, indent=4)

print(f"Success! {len(all_movies)} movies landed in raw_movies.json")

