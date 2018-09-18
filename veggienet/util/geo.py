import mapbox
from flask import current_app
import os

def geocode_address(address):
    geocoder = None
    if "MAPBOX_ACCESS_TOKEN" not in os.environ:
        geocoder = mapbox.Geocoder(access_token=current_app.config["MAPBOX_ACCESS_TOKEN"])
    else:
        geocoder = mapbox.Geocoder()
    geo_json = geocoder.forward(address).json()
    return geo_json["features"][0]['geometry']['coordinates']
