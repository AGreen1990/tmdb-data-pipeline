import pandas as pd
df = pd.read_csv("transformed_movies.csv")
print(len(df), df["movie_id"].nunique())
print(df[df.duplicated("movie_id", keep=False)].sort_values("movie_id").head(10))
