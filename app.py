import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

#Set up page layout
st.set_page_config(page_title="TMDB Movies Dashboard", page_icon="🍿", layout="wide")

st.title("🍿 TMDB Movies Dashboard")
st.markdown("Explore live, automated movie metrics pulled straight from Neon.")

#  --- 1.   CONNECT AND PULL DATA ---
@st.cache_data(ttl=3600)
def load_data():
    #1. Grab Neon connection string from Streamlit secrets
    db_url = st.secrets["DATABASE_URL"]

    #2. Establish the connection
    engine = create_engine(db_url)

    #3. Write a simple query to grab everything from the "movies" table
    query = "Select * FROM movies"

    #4. Use pandas to run the query and turn it into a dataframe

    df = pd.read_sql(query, con=engine)

    return df

#load  dataframe
df = load_data()

# --- Macro View: Gold Layer ----
st.header("🌍 The Macro View: Primary Genre Performance")
#st.markdown("Comparing overall **Average Rating** vs **Average popularity** across all primary genres. *(Hover over dots for details)*") - previous code - creates Bold caption same color as header 
st.caption("Comparing overall **Average Rating** vs **Average popularity** across all primary genres. *(Hover over dots for details)*") #creates greyed caption beneath - added for consistency

#streamlit scatter chart
#1 Group raw data by genre and calculate the averages and counts
genre_performance_df = df.groupby('primary_genre').agg(
    average_rating=('vote_average', 'mean'),
    average_popularity=('popularity','mean'),
    total_movies=('title', 'count')
).reset_index().round(2)  #rounds all numbers in dataframe to 2 decimals

chart_df = genre_performance_df.rename(columns={
    "average_rating": "Average Rating",
    "average_popularity": "Average Popularity",
    "primary_genre": "Primary Genre",
    "total_movies": "Total Movies" }) #added to change label appearance for all

st.scatter_chart(
    data=chart_df,
    x="Average Rating",
    y="Average Popularity",
    color="Primary Genre",
    size="Total Movies"
)

st.divider()

# ---3. Micro View: Silver Layer and Interactive Sidebar
st.header("🔬 The Micro View: Top 10 movies")

st.sidebar.header("Controls 🎛️")
#Create a list of uniue primary_primary_genres from the Silver database, and add "All" to the top
primary_genre_list = ["All"] + list(df['primary_genre'].unique())

#build dropdown menu
selected_primary_genre = st.sidebar.selectbox("Filter by primary genre:", primary_genre_list)

# -- 4. THE FILTER LOGIC --
if selected_primary_genre != "All":
    filtered_df = df[df['primary_genre'] == selected_primary_genre]
else:
    filtered_df = df

# --- 5. Top 10 Math
top_10_pop = filtered_df.nlargest(10, 'popularity').round({'popularity': 2}) #added .round code 
#renamed labels to be more formal for popularity and rating chart

chart_top_10_pop = top_10_pop.rename(columns={
    'title': 'Title',
    'popularity': 'Popularity'
})

top_10_rating = filtered_df.nlargest(10, 'vote_average').round({'vote_average': 2})
chart_top_10_rating = top_10_rating.rename(columns={
    'title': 'Title',
    'vote_average': 'Vote Average'
})
#6 --- Visualizations ---
st.markdown(f"### Currently viewing: **{selected_primary_genre}** Movies")

# Creates two side by side columns for charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Top Most Popular")
    st.caption("Score based on daily user views, votes, and watchlist additions on TMDB.") #adding context to TMDB popularity score
    st.bar_chart(data=chart_top_10_pop, x="Title", y="Popularity", horizontal=True, color="#ff4b4b")

with col2:
    st.subheader("⭐️ Top 10 Highest Rated")
    st.bar_chart(data=chart_top_10_rating, x="Title", y="Vote Average", horizontal=True, color="#00ff00")

#raw data expander at the bottom
with st.expander("🔎 View Raw Database Records"):
    st.dataframe(filtered_df, use_container_width=True)
