import json
import csv 

# 1. Read: Open the raw_movies.json file ("r" for read mode)
print("1. Reading raw JSON data...")
with open("raw_movies.json", "r") as file:
    raw_data = json.load(file)

movies_list =raw_data["results"]

print("2. Transforming and flattening data. . .")
cleaned_movies = []

# Loop through movies in list
for movie in movies_list:
    #Create new clean dictionary with only necessary fields
    #Use .get() so if movie is missing a field, it does not crash
    clean_movie = {
        "movie_id": movie.get("id"),
        "title": movie.get("title"),
        "release_date": movie.get("release_date"),
        "popularity": movie.get("popularity"),
        "vote_average": movie.get("vote_average")
    }
    cleaned_movies.append(clean_movie)

print("3. Saving to CSV format. . .")
#define column names
headers = ["movie_id", "title", "release_date", "popularity", "vote_average"]

#write cleaned data to CSV file
# newline= "" prevents empty rows between data, encoding="utf-8" handles special characters in movie titles
with open("transformed_movies.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=headers)

    writer.writeheader()   #writes column names as first row
    writer.writerows(cleaned_movies) #write all the movie data

print(f"Success! Transformed{len(cleaned_movies)} movies and saved to transformed_movies.csv")

# Last updated: June 30th. Ready for Load phase.