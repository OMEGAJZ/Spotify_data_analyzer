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

    #Convert the "Date and Time" column to a datetime data type
    df["Date and Time"] = pd.to_datetime(df["Date and Time"])

    # Create a new column "Time bin" that only contains the hour information from "Date and Time" column
    df["Time bin"] = df["Date and Time"].dt.hour

    # Group by "Time bin" and sum the "Playtime" column
    grouped_time_df = df.groupby("Time bin")["Playtime"].sum()
    
    # Gruppiere nach Monat und berechne den Mittelwert
    df_grouped_month = df.groupby(pd.Grouper(key='Date and Time', freq='M')).sum()

    # Konvertiere die Monatsnummern in Monatsnamen
    df_grouped_month.index = df_grouped_month.index.strftime('%B')

    # Apply the functions to the Playtime column and create new columns
    df["Playtime in hours"] = (df["Playtime"]/3600000)
    df["Playtime in minutes"] = (df["Playtime"]/60000)

    # Group by Artist and sum the Playtime columns
    grouped_artist_df = df.groupby("Artist")[["Playtime", "Playtime in hours", "Playtime in minutes"]].sum()

     # Group by Song title and sum the Playtime columns
    grouped_song_df = df.groupby("Song title")[["Playtime", "Playtime in hours", "Playtime in minutes"]].sum()

    # Sort by Playtime in minutes descending and get the top 50 rows
    sorted_artist_df = grouped_artist_df.sort_values("Playtime in minutes", ascending=False).head(50)
    sorted_song_df = grouped_song_df.sort_values("Playtime in minutes", ascending=False).head(50)

    # Display the top artists based on the selected number
    # Create a slider to allow the user to select the number of top artists to display
    num_top_artists = st.slider("Select the number of top artists to display:", 5, 50, 10, 5)
    st.subheader(f"Top {num_top_artists} streamed artists")
    top_artists_df = sorted_artist_df.head(num_top_artists)
    st.dataframe(top_artists_df.style.format(precision=0))
    st.write("Top Artists visualized")
    chart = alt.Chart(top_artists_df.reset_index()).mark_bar().encode(y=alt.Y("Artist", sort="-x"), x="Playtime in hours")
    st.altair_chart(chart)

    # Display the top songs based on the selected number
    # Create a slider to allow the user to select the number of top songs to display
    num_top_songs = st.slider("Select the number of top songs to display:", 5, 50, 10, 5)
    st.subheader(f"Top {num_top_songs} streamed songs")
    top_songs_df = sorted_song_df.head(num_top_songs)
    st.dataframe(top_songs_df.style.format(precision=0))
    st.write("Top Songs visualized")
    chart = alt.Chart(top_songs_df.reset_index()).mark_bar().encode(y=alt.Y("Song title", sort="-x", axis=alt.Axis(labelLimit=150)), x="Playtime in hours")
    st.altair_chart(chart)

else:
    st.markdown('''
    ## Introduction
    This is an automatic Spotify data analyzer web app, although it's still a work in progress.

    ## How to Request Your Spotify Data
    1. Open this [link](https://www.spotify.com/de/account/privacy/) and sign in to your spotify account
    2. Scroll down, check the box for "Account Data"
    3. Click on "Request"
    4. Receive your data as a json file from spotify
    5. Upload your data into the upload box on the sidebar
    6. Enjoy your data! 
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
    