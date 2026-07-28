import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

#Set up page layout
st.set_page_config(page_title="TMDB Movies Dashboard", page_icon="🍿", layout="wide")

st.title("🍿 TMDB Movies Dashboard")
st.markdown("Explore live, automated movie metrics pulled straight from Neon.")

#  --- 1.   CONNECT AND PULL DATA (SILVER & GOLD) ---
@st.cache_data
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



    #Pulls Silver Data (For individual titles)
    silver_query = "SELECT title, primary_genre, vote_average_AVERAGE, popularity FROM TMDB_PROJECT_DB.SILVER.CLEANED_MOVIES"
    silver_df = pd.read_sql(silver_query, conn)

    #Pulls Gold data (for aggregated primary_genre metrics)
    gold_query = "SELECT primary_genre, TOTAL_MOVIES, AVERAGE_RATING, AVERAGE_popularity FROM TMDB_PROJECT_DB.GOLD.primary_genre_METRICS_PHYSICAL"
    gold_df = pd.read_sql(gold_query, conn)

    return silver_df, gold_df

#load  dataframe
df = load_data()

# --- Macro View: Gold Layer ----
st.header("🌍 The Macro View: primary_genre Performance")
st.markdown("Comparing ovverall **Average Rating** vs **Average popularity** across all primary_genres. *(Hover over dots for details)*")

#streamlit scatter chart
#1 Group raw data by genre and calculate the averages and counts
genre_performance_df = df.groupby('primary_genre').agg(
    average_rating=('vote_average', 'mean'),
    average_popularity=('popularity','mean'),
    total_movies=('title', 'count')
).reset_index()

st.scatter_chart(
    data=genre_performance_df,
    x="average_rating",
    y="average_popularity",
    color="primary_genre",
    size="total_movies"
)

st.divider()

# ---3. Micro View: Silver Layer and Interactive Sidebar
st.header("🔬 The Micro View: Top 10 movies")

st.sidebar.header("Controls 🎛️")
#Create a list of uniue primary_primary_genres from the Silver database, and add "All" to the top
primary_genre_list = ["All"] + list(df['primary_genre'].unique())

#build dropdown menu
selected_primary_genre = st.sidebar.selectbox("Filter by primary_genre:", primary_genre_list)

# -- 4. THE FILTER LOGIC --
if selected_primary_genre != "All":
    filtered_df = df[df['primary_genre'] == selected_primary_genre]
else:
    filtered_df = df

# --- 5. Top 10 Math
top_10_pop = filtered_df.nlargest(10, 'popularity')
top_10_rating = filtered_df.nlargest(10, 'vote_average')

#6 --- Visualizations ---
st.markdown(f"### Currently viewing: **{selected_primary_genre}** Movies")

# Creates two side by side columns for charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Top Most Popular")
    st.bar_chart(data=top_10_pop, x="title", y="popularity", horizontal=True, color="#ff4b4b")

with col2:
    st.subheader("⭐️ Top 10 Highest Rated")
    st.bar_chart(data=top_10_rating, x="title", y="vote_average", horizontal=True, color="#00ff00")

#raw data expander at the bottom
with st.expander("🔎 View Raw Database Records"):
    st.dataframe(filtered_df, use_container_width=True)
