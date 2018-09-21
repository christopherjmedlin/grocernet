import mapbox
from flask import current_app
import os


def geocode_address(address):
    geocoder = None
    geocoder = mapbox.Geocoder()
    geo_json = geocoder.forward(address).json()
    feature = geo_json["features"][0]

    return (feature["place_name"], feature['geometry']['coordinates'])


def parse_postgis_point(point):
    nums = point[6:-1].split()
    try:
        return [float(nums[0]), float(nums[1])]
    except Exception:
        raise ValueError("Invalid PostGIS point.")
