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
    silver_query = "SELECT TITLE, GENRE, VOTE_AVERAGE, POPULARITY FROM TMDB_PROJECT_DB.SILVER.CLEANED_MOVIES"
    silver_df = pd.read_sql(silver_query, conn)

    #Pulls Gold data (for aggregated genre metrics)
    gold_query = "SELECT GENRE, TOTAL_MOVIES, AVERAGE_RATING, AVERAGE_POPULARITY FROM TMDB_PROJECT_DB.GOLD.GENRE_METRICS_PHYSICAL"
    gold_df = pd.read_sql(gold_query, conn)

    return silver_df, gold_df

#load  dataframe
df = load_data()

# --- Macro View: Gold Layer ----
st.header("🌍 The Macro View: Genre Performance")
st.markdown("Comparing ovverall **Average Rating** vs **Average Popularity** across all genres. *(Hover over dots for details)*")

#streamlit's native scatter chart
st.scatter_chart(
    data=gold_df,
    x="AVERAGE_RATING",
    y="AVERAGE_POPULARITY",
    color="GENRE",
    size="TOTAL_MOVIES"
)

st.divider()

# ---3. Micro View: Silver Layer and Interactive Sidebar
st.header("🔬 The Micro View: Top 10 movies")

st.sidebar.header("Controls 🎛️")
#Create a list of uniue genres from the Silver database, and add "All" to the top
genre_list = ["All"] + list(silver_df['GENRE'].unique())

#build dropdown menu
selected_genre = st.sidebar.selectbox("Filter by Genre:", genre_list)

# -- 4. THE FILTER LOGIC --
if selected_genre != "All":
    filtered_df = silver_df[silver_df['GENRE'] == selected_genre]
else:
    filtered_df = silver_df

# --- 5. Top 10 Math
top_10_pop = filtered_df.nlargest(10, 'POPULARITY')
top_10_rating = filtered_df.nlargest(10, 'VOTE_AVERAGE')

#6 --- Visualizations ---
st.markdown(f"### Currently viewing: **{selected_genre}** Movies")

# Creates two side by side columns for charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Top Most Popular")
    st.bar_chart(data=top_10_pop, x="TITLE", y="POPULARITY", horizontal=True, color="#ff4b4b")

with col2:
    st.subheader("⭐️ Top 10 Highest Rated")
    st.bar_chart(data=top_10_rating, x="TITLE", y="VOTE_AVERAGE", horizontal=True, color="#00ff00")

#raw data expander at the bottom
with st.expander("🔎 View Raw Database Records"):
    st.dataframe(filtered_df, use_container_width=True)
