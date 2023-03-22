from bidict import bidict
import numpy as np
import pandas as pd
import pydeck
import streamlit as st
from routes import load_routes_definition, convert_routes_to_pathlayer
#from ipywidgets import HTML

def each_cons(x: list, size: int) -> list:
    return [x[i:i+size] for i in range(len(x)-size+1)]

st.title("Foo")


ICON_DATA = {
    "url": "https://img.icons8.com/plasticine/100/000000/marker.png",
    "width": 128,
    "height": 128,
    "anchorY": 128,
}

stops = pd.read_csv(
    "data/hokkaido_chuo/stops.txt",
    usecols=("stop_id", "stop_name", "stop_lat", "stop_lon"))
# st.write(bus_stops)
stops_merged = stops.groupby("stop_name").agg({
    #"stop_id": ",".join,
    "stop_lat": np.mean,
    "stop_lon": np.mean,
}).reset_index()
stops_merged["tooltip"] = stops_merged["stop_name"]

#route_names = pd.read_csv(
#    "data/hokkaido_chuo/routes.txt",
#    usecols=("route_id", "route_long_name", ))

stop_times = pd.read_csv(
    "data/hokkaido_chuo/stop_times.txt",
    usecols=("trip_id", "arrival_time", "stop_id", "stop_sequence", ))
routes = pd.read_csv(
    "data/hokkaido_chuo/routes.txt",
    usecols=("route_id", "route_long_name", ))
trips = pd.read_csv(
    "data/hokkaido_chuo/trips.txt",
    usecols=("route_id", "trip_id", ))
all = stop_times[:10].merge(stops, on="stop_id", how="left")
all = all.merge(trips, on="trip_id", how="left")
all = all.merge(routes, on="route_id", how="left")
st.write("時刻表", all)

st.markdown("---")

stops_by_name = all.groupby("stop_name")
stop_count = stops_by_name.ngroups
stop_names_dict = bidict()
for i, k in enumerate(stops_by_name.groups.keys()):
    stop_names_dict[i] = k
st.write(stops_by_name.groups.keys(), stop_count, stop_names_dict)

stops_by_trip = all.groupby("trip_id")
adjacency = np.zeros((stop_count, stop_count))
for group_name, group in stops_by_trip:
    # print(group_name, group)
    for n1, n2 in each_cons(list(group["stop_name"]), 2):
        i = stop_names_dict.inverse[n1]
        j = stop_names_dict.inverse[n2]
        adjacency[i, j] += 1
        adjacency[j, i] += 1

st.write("groupby", stops_by_trip.groups, adjacency)

st.markdown("---")

routes = load_routes_definition()
pathlayer_data = convert_routes_to_pathlayer(routes, stops_merged)

# st.write(routes)
# st.write(pathlayer_data)

stops_merged["icon_data"] = None
icon_data_col = stops_merged.columns.get_loc("icon_data")
for i in stops_merged.index:
    stops_merged.iat[i, icon_data_col] = ICON_DATA

st.write(stops_merged)

icon_layer = pydeck.Layer(
    type="IconLayer",
    data=stops_merged,
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

st.pydeck_chart(deck)

# deck.to_html("out.html")
