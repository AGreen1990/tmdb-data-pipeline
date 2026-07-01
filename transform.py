import json
import csv 

# 1. Read: Open the raw_movies.json file ("r" for read mode)
print("1. Reading raw JSON data...")
with open("raw_movies.json", "r") as file:
    raw_data = json.load(file)

movies_list =raw_data["results"]

print("2. Transforming and flattening data. . .")
cleaned_movies = []

#TMDB genre mapping 
genre_map = {
    28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy", 
    80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family", 
    14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance", 878: "Science Fiction",
    10770: "TV Movie", 53: "Thriller", 10752: "War", 37: "Western"
}
# Loop through movies in list
for movie in movies_list:

    #1. grabs list of genre_ids (default to empty list if missing)
    genre_ids = movie.get("genre_ids",[])
    
    #2 Grabs first ID in the list, set to None if empty
    primary_genre_id = genre_ids[0] if len(genre_ids) > 0 else None

    #3. translate the id to name using genre_map, default to unknown
    genre_name = genre_map.get(primary_genre_id, "Unknown")                   
                        
    #Create new clean dictionary with only necessary fields
    #Use .get() so if movie is missing a field, it does not crash
    clean_movie = {
        "movie_id": movie.get("id"),
        "title": movie.get("title"),
        "release_date": movie.get("release_date"),
        "popularity": movie.get("popularity"),
        "vote_average": movie.get("vote_average"),
        "primary_genre": genre_name
    }
    cleaned_movies.append(clean_movie)

print("3. Saving to CSV format. . .")
#define column names
headers = ["movie_id", "title", "release_date", "popularity", "vote_average", "primary_genre"]

#write cleaned data to CSV file
# newline= "" prevents empty rows between data, encoding="utf-8" handles special characters in movie titles
with open("transformed_movies.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=headers)

    writer.writeheader()   #writes column names as first row
    writer.writerows(cleaned_movies) #write all the movie data

print(f"Success! Transformed{len(cleaned_movies)} movies and saved to transformed_movies.csv")

# Last updated: June 30th. Ready for Load phase.