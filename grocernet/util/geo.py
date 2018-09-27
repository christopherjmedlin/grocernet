import mapbox
import os

def geocode_address(address):
    """
    Geocodes address with Mapbox Geocoding API, then returns data in a
    a tuple of the format ('place name', [x, y])

    Returns None if Mapbox Geocoding API returns nothing of value.
    """
    geocoder = None
    geocoder = mapbox.Geocoder()
    geo_json = geocoder.forward(address).json()

    if "features" not in geo_json or len(geo_json["features"]) == 0:
        return None
    feature = geo_json["features"][0]

    return (feature["place_name"], feature['geometry']['coordinates'])


def parse_postgis_point(point):
    nums = point[6:-1].split()
    try:
        return [float(nums[0]), float(nums[1])]
    except Exception:
        raise ValueError("Invalid PostGIS point.")


def get_mapbox_static_url(longitude, latitude):
    if "MAPBOX_ACCESS_TOKEN" not in os.environ:
        return None
    url = "https://api.mapbox.com/styles/v1/mapbox/streets-v10/static/" + \
          str(longitude) + "," + str(latitude) + ",17,0,60/250x250?access_token=" + \
          os.environ["MAPBOX_ACCESS_TOKEN"]
    return url
