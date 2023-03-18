import pandas as pd
import pydeck
import streamlit as st
import json

st.title("Foo")

bus_stops = pd.read_csv(
    "data/hokkaido_chuo/stops.txt",
    usecols=("stop_name", "stop_lat", "stop_lon"))

icon_data = {
    "url": "https://img.icons8.com/plasticine/100/000000/marker.png",
    "width": 128,
    "height": 128,
    "anchorY": 128,
}

#icon_series = pd.Series(icon_data, index=range(len(bus_stops)))
#st.write(icon_series)

#bus_stops["icon_data"] = json.dumps(icon_data)
bus_stops['icon_data'] = None
for i in bus_stops.index:
    # bus_stops['icon_data'][i] = icon_data
    bus_stops.iat[i, -1] = icon_data

#bus_stops.loc[:, 'icon_data'] = None
#bus_stops.loc[:, 'icon_data'] = icon_data
#bus_stops.iloc[:, -1] = icon_data

st.write(bus_stops)
# st.write(bus_stops.dtypes)

icon_layer = pydeck.Layer(
    type="IconLayer",
    data=bus_stops,
    get_icon="icon_data",
    get_position=["stop_lon", "stop_lat"],
    get_size=4,
    size_scale=15,
    pickable=True,
)

deck = pydeck.Deck(
    layers=[icon_layer],
    map_style="road",
    initial_view_state=pydeck.ViewState(
        latitude=43.08984839132553,
        longitude=141.27750554973517,
        zoom=11,
        pitch=0,
    ),
    tooltip={"text": "{stop_name}"})

st.pydeck_chart(deck)

#deck.to_html("out.html")
