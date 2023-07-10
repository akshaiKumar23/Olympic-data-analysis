import streamlit as st
import preprocessor
import pandas as pd
import helper

df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")
df = preprocessor.preProcess(df, region_df)

st.sidebar.title("Olympics Analysis")

user_menu = st.sidebar.radio(
    "Select an Option",
    (
        "Medal Tally",
        "Overall Analysis",
        "Country-wise Analysis",
        "Athlete wise Analysis",
    ),
)

if user_menu == "Medal Tally":
    st.sidebar.header("Medal Tally")
    years, country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)
    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
    st.dataframe(medal_tally)
