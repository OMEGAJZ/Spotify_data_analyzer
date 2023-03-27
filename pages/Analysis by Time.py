import numpy as np
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import base64

# Create a title and a sidebar
st.set_page_config(
    page_title="Spotify data analyzer",
    page_icon="https://symbl-world.akamaized.net/i/webp/df/6766b8646eb16b761cb590d752e6b2.webp",
    layout="centered",
    initial_sidebar_state="expanded")

st.header("Spotify data analyzer")
st.caption("Where words fail, music speaks")

image = Image.open('spotify_small.png')

st.sidebar.image(image, caption='Listening is everything')


# Ask the user to upload a json file
uploaded_file = st.sidebar.file_uploader("", type="json")

# If the user uploads a file, process it and display the results
if uploaded_file is not None:
    # Read the json file into a pandas dataframe
    df = pd.read_json(uploaded_file)

    # Change the column names according to the user's request
    df.columns = ["Date and Time", "Artist", "Song title", "Playtime"]

    # Apply the functions to the Playtime column and create new columns
    df["Playtime in hours"] = (df["Playtime"]/3600000)
    df["Playtime in minutes"] = (df["Playtime"]/60000)

    #Convert the "Date and Time" column to a datetime data type
    df["Date and Time"] = pd.to_datetime(df["Date and Time"])

    # Create a new column "Time bin" that only contains the hour information from "Date and Time" column
    df["Time bin"] = df["Date and Time"].dt.hour

    # Group by "Time bin" and sum the "Playtime" column
    grouped_time_df = df.groupby("Time bin")["Playtime"].sum()

    #convert the data to datetime format
    df['month bin'] = pd.to_datetime(df['Date and Time'])

    #define bins for months
    bins = [0, 1, 2, 3, 4, 5, 6, 7, 8 ,9 ,10 ,11 ,12]

    #create a new column for month
    df['month bin'] = df['Date and Time'].dt.month

    #group by month and sum playtime in hours
    grouped = df.groupby(pd.cut(df['month bin'], bins=bins))['Playtime in hours'].sum()

    # Datetime-Spalte als Index setzen
    df.index = pd.to_datetime(df['Date and Time'])

    # Gruppieren nach Wochentag und Summieren von Playtime in Hours
    grouped = df.groupby(df.index.weekday)['Playtime in hours'].sum()

    # Umbenennen der Wochentage
    grouped.index = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']

    # Create a new column "weekday" based on the "Date and Time" column
    df['weekday'] = df['Date and Time'].dt.day_name()

    # Create a bar chart with the data from the "weekday" column
    st.header("You loved to listen to music on these days!")
    st.write("Streaming hours distribution")
    fig3 = alt.Chart(df).mark_bar(size=105).encode(
        alt.X("weekday", sort=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], title="Day of the Week", axis=alt.Axis(labelAngle=0)),
        alt.Y("sum(Playtime in hours)", title="Total Playtime (h)")
    ).properties(width=850, height=370)
    st.altair_chart(fig3)

    # Create a histogram with the data from the "Month bin" column
    st.header("You loved to listen to music in these months!")
    st.write("Streaming hours distribution")
    fig1 = alt.Chart(df).mark_bar().encode(
        alt.X("month bin",  bin=alt.Bin(step=1), title="Month of the year"),
        alt.Y("sum(Playtime in hours)", title="Total Playtime (h)")
    ).properties(width=850, height=400)
    st.altair_chart(fig1)

    # Create a histogram with the data from the "Time bin" column
    st.header("You loved to listen to music at these times!")
    st.write("Streaming hours distribution")
    fig0 = alt.Chart(df).mark_bar().encode(
        alt.X("Time bin", bin=alt.Bin(step=1), title="Hour of the day"),
        alt.Y("sum(Playtime in hours)", title="Total Playtime (h)")
    ).properties(width=850, height=400)
    st.altair_chart(fig0)

else:
    st.markdown('''
    ## Introduction
    This is an automatic Spotify data analyzer web app, although it's still a work in progress.

    ## How to Request Your Spotify Data
    1. Open this [link](https://www.spotify.com/de/account/privacy/) and sign in to your spotify account
    2. Scroll down, check the box for "Account Data"
    3. Click on "Request"
    4. You will receive few files from Spotify. Take the one with the name "StreamingHistory0"
    5. Upload your data into the upload box on the sidebar
    6. Enjoy your insights! 
    ''')

    st.markdown('''
    #### Interested what your data could look like? Download my example file and try it yourself!
    ''')

    # Load Json
    with open("spotify_data_example.json", "r") as f:
        data = f.read()

    # Convert to base64
    b64 = base64.b64encode(data.encode()).decode()

    # Create DL-Link
    href = f'<a href="data:file/json;base64,{b64}" download="spotify_data_example.json">Download example spotify data json file</a>'

    # Import Dl-Link
    st.markdown(href, unsafe_allow_html=True)

    st.write("Feel free to share this web app and leave some feedback on my Github, many thanks! <3")
    
