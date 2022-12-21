import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# st.title("Hello World")
# st.markdown("## My first streamlit dashboard!")

DATA_URL = ("C:\\Users\\cromero\\Dropbox\\Learning\\Build_a_data_app_streamlit\\Motor_Vehicle_Collisions_-_Crashes.csv")

st.title("Motor Vehicle Collisions in New York City")
st.markdown("This application is a streamlit dashboard that can be used"
            "to analyze motor vehicle collisions in NYC 🗽💥🚗")

'''
It loads the data from the URL, parses the date/time column, and drops any rows that don't have a latitude or longitude

:param nrows: number of rows to read from the dataset
:return: A dataframe with the data from the URL
'''


@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data


# Asking how many people are injured in a collision?
# Loading the data from the URL, parsing the date/time column, and dropping any rows that don't have a latitude or
# longitude

data = load_data(100000)
st.header("Where are the most people injured in NYC")
injured_people = st.slider("Number of persons injured in vehicle collisions", 0, 19)
# to filter data in pandas
st.map(data.query("injured_persons >= @injured_people")[['latitude', "longitude"]].dropna(how="any"))

# How many collisions occur during a given time of the day?
st.header("How many collisions occur at a given time of a day?")
# hour = st.sidebar.slider("Hour to look at", 0, 24) # to visualize the slider on the side menu.
hour = st.slider("Hour to look at", 0, 24)
data = data[data["date/time"].dt.hour == hour]

# how many collisions given a time
st.markdown("Vehicle collisions between %i:00 and %i:00" % (hour, (hour + 1) % 24))
midpoint = (np.average(data['latitude']), np.average(data['longitude']))
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={"latitude": midpoint[0], "longitude": midpoint[1], "zoom": 11, "pitch": 50}
))


# Creating a checkbox that when checked will show the raw data.
if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)
