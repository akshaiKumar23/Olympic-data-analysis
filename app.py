import streamlit as st
import preprocessor
import helper
import pandas as pd
import plotly.express as px
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy
import plotly.figure_factory as ff


df = pd.read_csv("athlete_events.csv")
region_df = pd.read_csv("noc_regions.csv")
df = preprocessor.preProcess(df, region_df)

st.sidebar.title("Olympics Analysis")
st.sidebar.image("https://cdn.wallpapersafari.com/0/72/S307o5.jpg")
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

    if selected_year == "Overall" and selected_country == "Overall":
        st.title("Overall Tally")

    if selected_year == "Overall" and selected_country != "Overall":
        st.title(selected_country + " Overall Performance")

    if selected_year != "Overall" and selected_country == "Overall":
        st.title("Medal Tally in " + str(selected_year))

    if selected_year != "Overall" and selected_country != "Overall":
        st.title(
            selected_country + " Performance in " + str(selected_year) + " Olympics"
        )
    st.table(medal_tally)


if user_menu == "Overall Analysis":
    editions = df["Year"].unique().shape[0] - 1
    cities = df["City"].unique().shape[0]
    sports = df["Sport"].unique().shape[0]
    events = df["Event"].unique().shape[0]
    athletes = df["Name"].unique().shape[0]
    nations = df["region"].unique().shape[0]

    st.title("Top Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Host")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Events")
        st.title(editions)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    dict = pickle.load(open("nations_over_time.pkl", "rb"))
    nations_over_time = pd.DataFrame(dict)
    fig = px.line(nations_over_time, x="Edition", y="No of Countries")
    st.header("Participating Nations Over the Years")
    st.plotly_chart(fig)

    dict1 = pickle.load(open("events_over_time.pkl", "rb"))
    events_over_time = pd.DataFrame(dict1)
    fig1 = px.line(events_over_time, x="Edition", y="Event")
    st.header("No of Events Over the Years")
    st.plotly_chart(fig1)

    dict2 = pickle.load(open("athletes_over_time.pkl", "rb"))
    athletes_over_time = pd.DataFrame(dict2)
    fig2 = px.line(athletes_over_time, x="Edition", y="Athletes")
    st.header("Athletes Participating Over the Years")
    st.plotly_chart(fig2)

    st.title("No of Events Over time(Every Sport)")
    fig, ax = plt.subplots(figsize=(30, 30))
    x = df.drop_duplicates(["Year", "Sport", "Event"])
    sns.heatmap(
        x.pivot_table(index="Sport", columns="Year", values="Event", aggfunc="count")
        .fillna(0)
        .astype("int"),
        annot=True,
    )

    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")

    selected_sport = st.selectbox("Select a Sport", sport_list)
    x = pickle.load(open("best_athletes2.pkl", "rb"))
    x = pd.DataFrame(x)
    if selected_sport != "Overall":
        x = x[x["Sport"] == selected_sport]

    st.table(x.head(15))

if user_menu == "Country-wise Analysis":
    st.sidebar.title("Country-wise Analysis")

    country_list = df["region"].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox("Select a Country", country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally over the years")
    st.plotly_chart(fig)

    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))

    ax = sns.heatmap(pt, annot=True)
    st.title(selected_country + " excels in the following sports")
    st.pyplot(fig)

    st.title("Top 10 Athletes of " + selected_country)
    x = pickle.load(open("best_athletes2.pkl", "rb"))
    x = pd.DataFrame(x)
    x = x[x["region"] == selected_country][["Name", "Medals", "Sport"]]

    st.table(x.head(15))

if user_menu == "Athlete wise Analysis":
    athlete_df = df.drop_duplicates(subset=["Name", "region"])
    x = athlete_df["Age"].dropna()
    x1 = athlete_df[athlete_df["Medal"] == "Gold"]["Age"].dropna()
    x2 = athlete_df[athlete_df["Medal"] == "Silver"]["Age"].dropna()
    x3 = athlete_df[athlete_df["Medal"] == "Bronze"]["Age"].dropna()

    hist_data = [x, x1, x2, x3]
    group_labels = [
        "Overall Age",
        "Gold Medalist",
        "Silver Medalist",
        "Bronze Medalist",
    ]

    fig = ff.create_distplot(
        hist_data,
        group_labels,
        show_hist=False,
        show_rug=False,
    )
    fig.update_layout(autosize=False, width=800, height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = [
        "Basketball",
        "Judo",
        "Football",
        "Tug-Of-War",
        "Athletics",
        "Swimming",
        "Badminton",
        "Sailing",
        "Gymnastics",
        "Art Competitions",
        "Handball",
        "Weightlifting",
        "Wrestling",
        "Water Polo",
        "Hockey",
        "Rowing",
        "Fencing",
        "Shooting",
        "Boxing",
        "Taekwondo",
        "Cycling",
        "Diving",
        "Canoeing",
        "Tennis",
        "Golf",
        "Softball",
        "Archery",
        "Volleyball",
        "Synchronized Swimming",
        "Table Tennis",
        "Baseball",
        "Rhythmic Gymnastics",
        "Rugby Sevens",
        "Beach Volleyball",
        "Triathlon",
        "Rugby",
        "Polo",
        "Ice Hockey",
    ]

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df["Sport"] == sport]
        x.append(temp_df[temp_df["Medal"] == "Gold"]["Age"].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=900, height=600)
    st.title("Distribution of Age Respective to Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df["Sport"].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, "Overall")

    selected_sport = st.selectbox("Select a Sport", sport_list)
    fig, ax = plt.subplots(figsize=(10, 10))

    athlete_df = helper.weight_v_height(df, selected_sport)
    ax = sns.scatterplot(
        athlete_df, x="Weight", y="Height", hue="Medal", style="Sex", s=100
    )
    st.title("Weight Vs Height")
    st.pyplot(fig)

    final = helper.men_v_women(df)
    fig = px.line(final, x="Year", y=["Men", "Women"])
    st.title("Men Vs Women Over the Years")
    st.plotly_chart(fig)
