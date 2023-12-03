import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

def app():

    DATA_URL = (
    "/Users/sumonaung/Desktop/env/multipage/apps/Motor_Vehicle_Collisions_-_Crashes 2.csv"
    )

    st.markdown("<h1 style='text-align: center; color: white;'>Geographic Data</h1>", unsafe_allow_html=True)

    @st.cache(persist=True)
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[["CRASH DATE", "CRASH TIME"]])
        data.dropna(subset=["LATITUDE", "LONGITUDE"], inplace=True)
        data.drop(data[data['LATITUDE'] == 0].index, inplace=True)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data.rename(columns={'crash date_crash time': 'date/time'}, inplace=True)
        data.rename(columns={'number of persons injured': 'injured_persons'}, inplace=True)
        data.rename(columns={'number of pedestrians injured': 'injured_pedestrians'}, inplace=True)
        data.rename(columns={'number of cyclist injured': 'injured_cyclists'}, inplace=True)
        data.rename(columns={'number of motorist injured': 'injured_motorists'}, inplace=True)
        return data

    data = load_data(60000)

    st.sidebar.header("Business Licence Map")
    #st.header("Number of Business Licences")

    st.sidebar.header("Filter Parameters")
    st.sidebar.header("Choose the most popular licence")
#injured_people = st.sidebar.slider("# Person injured in Collisions", 0, 9)
    injured_people = st.sidebar.number_input("Number of Licence", step=1, min_value=0, max_value=9, value=1)
    st.map(data.query('injured_persons > @injured_people')[["latitude", "longitude"]].dropna(how="any"))

    st.sidebar.header("Licence Issued within One Day")
    hour = st.sidebar.number_input("Insert TIME-HOUR", step=1, min_value=0, max_value=24, value=1)

    data = data[data['date/time'].dt.hour == hour]
    st.header(" No of Licence between %i:00 and %i:00 " % (hour, (hour + 1) % 24))

    midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 12,
            "pitch": 50,

        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data[['date/time', 'latitude', 'longitude']],
                get_position=["longitude", "latitude"],
                auto_highlight=True,
                radius=100,
                extruded=True,
                pickable=True,
                elevation_scale=4,
                elevation_range=[0, 1000],
            ),
        ],
    ))

    st.header("Histogram by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
    filtered = data[
        (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))
        ]

    hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0, 60))[0]
    chart_data = pd.DataFrame({"minute": range(60), "crashes": hist})

    fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
    st.write(fig)

    st.sidebar.header("Licence Comparison")
    st.header("Most Popular Business Licences")
    select = st.sidebar.selectbox('Affected type of person', ['Pedestrians', 'Cyclist', 'Motorists'])

    if select == 'Pedestrians':
        st.write(data.query("injured_pedestrians >= 1")[["on street name", "injured_pedestrians"]].sort_values(
            by=['injured_pedestrians'], ascending=False).dropna(how="any")[:7])

    elif select == 'Cyclists':
        st.write(
            data.query("injured_cyclists >= 1")[["on street name", "injured_cyclists"]].sort_values(
                by=['injured_cyclists'], ascending=False).dropna(how="any")[:7])

    else:
        st.write(data.query("injured_motorists >= 1")[["on street name", "injured_motorists"]].sort_values(
            by=['injured_motorists'], ascending=False).dropna(how="any")[:7])

    if st.checkbox("Show Data", False):
        st.subheader('Raw Data')
        st.write(data)

    #st.sidebar.markdown("libraries used: **streamlit**, **pandas**, **numpy**, **pydeck**, **plotly**")
    #st.sidebar.markdown("**Dataset:** Rows: 1.69M  Columns: 29")
    #st.sidebar.markdown("Update: November 30, 2022")
