import pandas as pd
import pydeck
import streamlit as st

st.title("Foo")

bus_stops = pd.read_csv("hokkaido_chuo/stops.txt")
st.write(bus_stops)

icon_data = {
    "url": "https://img.icons8.com/plasticine/100/000000/marker.png",
    "width": 128,
    "height": 128,
    "anchorY": 128,
}
bus_stops['icon_data'] = None
for i in bus_stops.index:
    bus_stops['icon_data'][i] = icon_data

icon_layer = pydeck.Layer(
    type="IconLayer",
    data=bus_stops,
    get_icon='icon_data',
    get_position=["stop_lon", "stop_lat"],
    pickable=True,
)

deck = pydeck.Deck(
    layers=[icon_layer],
    map_style='mapbox://styles/mapbox/streets-v11',
    initial_view_state=pydeck.ViewState(
        latitude=43.08984839132553,
        longitude=141.27750554973517,
        zoom=11,
        pitch=0,
    ),
    tooltip={"text": "{stop_name}"})
st.pydeck_chart(deck)
