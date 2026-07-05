import streamlit as st
import snowflake.connector
import pandas as pd
import os
from dotenv import load_dotenv

#load the local .env file to grab snowflake keys
load_dotenv()

#set up visual configuration of web page
st.set_page_config(page_title="TMDB Dashboard", page_icon="🍿", layout="wide")

st.title("🍿 TMDB Movies Trends Dashboard")
st.markdown("This dashboard pulls live, aggregated metrics directly from the Snowflake Gold Layer. ")

# @st.cache_data tells streamlit to remember the data so it 
# doesn't drain your Snowflake computecredits every time you click a button

@st.cache_data
def load_data():
    print("Connecting to Snowflake to fetch Gold data. . . ")
    conn = snowflake.connector.connect(
        user=os.getenv("SF_USER"),
        password=os.getenv("SF_PASSWORD"),
        account=os.getenv("SF_ACCOUNT"),
        warehouse="COMPUTE_WH",
        database="TMDB_PROJECT_DB",
        schema="GOLD"
    )

    # Pandas allows you to grab a SQL table and turn it into a readable format

    query = "SELECT * FROM TMDB_PROJECT_DB.GOLD.GENRE_METRICS"
    df = pd.read_sql(query, conn)

    conn.close()
    return df

# Run function to fetch data
df = load_data()

#----------------------------------------------------------
# VISUALIZATION SECTION
#----------------------------------------------------------

# Creates two side by side columns on webpage
col1, col2 = st.columns(2)

with col1:
    st.subheader("Data Overview (Gold View)")
    #displays raw dataframe as clean table
    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("Total Movies Per Genre")
    # Builds a bar chrt mapping the Genre to the Total Movies count
    st.bar_chart(data=df, x="GENRE", y="TOTAL_MOVIES")

st.divider()

st.subheader("Average Rating vs. Popularity")
#Creates scatterplot by layer two line charts over genre
st.line_chart(data=df, x="GENRE", y=["AVERAGE_RATING", "AVERAGE_POPULARITY"])