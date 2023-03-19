import numpy as np
import pandas as pd
import pydeck
import streamlit as st
from routes import load_routes_definition, convert_routes_to_pathlayer
#from ipywidgets import HTML

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
bus_stops["tooltip"] = bus_stops["stop_name"]

#route_names = pd.read_csv(
#    "data/hokkaido_chuo/routes.txt",
#    usecols=("route_id", "route_long_name", ))

routes = load_routes_definition()
pathlayer_data = convert_routes_to_pathlayer(routes, bus_stops)

# st.write(routes)
# st.write(pathlayer_data)

bus_stops["icon_data"] = None
icon_data_col = bus_stops.columns.get_loc("icon_data")
for i in bus_stops.index:
    bus_stops.iat[i, icon_data_col] = ICON_DATA

st.write(bus_stops)

def on_click():
    print('Testing...')
    st.write("TEST TEST")

icon_layer = pydeck.Layer(
    type="IconLayer",
    data=bus_stops,
    get_icon="icon_data",
    get_position=["stop_lon", "stop_lat"],
    get_size=4,
    size_scale=15,
    pickable=True,
    on_click=on_click,
)
path_layer = pydeck.Layer(
    type="PathLayer",
    data=pathlayer_data,
    pickable=True,
    get_color="color",
    width_scale=1,
    width_min_pixels=5,
    get_path="path",
    get_width="width",
)

deck = pydeck.Deck(
    layers=(icon_layer, path_layer),
    map_style="road",
    initial_view_state=pydeck.ViewState(
        latitude=43.021416023920374,
        longitude=141.403294639492,
        zoom=11,
        pitch=0,
    ),
    tooltip={
        "text": "{tooltip}",
        "style": {}
    })


def filter_by_viewport(widget_instance, payload):
    print(widget_instance, payload)


#deck.deck_widget.on_click(filter_by_viewport)

st.pydeck_chart(deck)

# deck.to_html("out.html")
