import numpy as np
import pandas as pd
import pydeck
import streamlit as st
from routes import load_routes_definition, convert_routes_to_pathlayer

st.title("Foo")


ICON_DATA = {
    "url": "https://img.icons8.com/plasticine/100/000000/marker.png",
    "width": 128,
    "height": 128,
    "anchorY": 128,
}

bus_stops = pd.read_csv(
    "data/hokkaido_chuo/stops.txt",
    usecols=("stop_id", "stop_name", "stop_lat", "stop_lon"))
# st.write(bus_stops)
bus_stops = bus_stops.groupby("stop_name").agg({
    #"stop_id": ",".join,
    "stop_lat": np.mean,
    "stop_lon": np.mean,
}).reset_index()

#route_names = pd.read_csv(
#    "data/hokkaido_chuo/routes.txt",
#    usecols=("route_id", "route_long_name", ))

routes = load_routes_definition()
pathlayer_data = convert_routes_to_pathlayer(routes, bus_stops)

st.write(routes)
st.write(pathlayer_data)

bus_stops["icon_data"] = None
icon_data_col = bus_stops.columns.get_loc("icon_data")
for i in bus_stops.index:
    bus_stops.iat[i, icon_data_col] = ICON_DATA

st.write(bus_stops)

icon_layer = pydeck.Layer(
    type="IconLayer",
    data=bus_stops,
    get_icon="icon_data",
    get_position=["stop_lon", "stop_lat"],
    get_size=4,
    size_scale=15,
    pickable=True,
)
path_layer = pydeck.Layer(
    type="PathLayer",
    data=pathlayer_data,
    pickable=True,
    get_color="color",
    width_scale=20,
    width_min_pixels=2,
    get_path="path",
    get_width=5,
)

deck = pydeck.Deck(
    layers=(icon_layer, path_layer),
    map_style="road",
    initial_view_state=pydeck.ViewState(
        latitude=43.08984839132553,
        longitude=141.27750554973517,
        zoom=11,
        pitch=0,
    ),
    tooltip={"text": "{stop_name}{name}"})
st.pydeck_chart(deck)

#deck.to_html("out.html")
