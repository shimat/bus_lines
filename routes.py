import json
import pandas as pd
from typing import Any, TypeAlias

RoutesDefinition: TypeAlias = list[dict[str, Any]]


def load_routes_definition() -> RoutesDefinition:
    with open("data/routes.json", encoding="utf-8-sig") as f:
        return json.load(f)["routes"]


def convert_routes_to_pathlayer(routes: RoutesDefinition, bus_stops: pd.DataFrame) -> list[dict[str, Any]]:
    ret = []
    for route in routes:
        obj = {}
        obj["name"] = route["name"]
        obj["color"] = "red"
        obj["width"] = 1
        obj["path"] = [
            tuple(bus_stops.query("stop_name == @stop_name")[["stop_lon", "stop_lat"]].values[0]) for stop_name in route["stops"]
        ]
        obj["tooltip"] = route["name"]
        ret.append(obj)
    return ret
