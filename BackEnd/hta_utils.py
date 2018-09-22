import urllib.request
import json
import pandas as pd
import geopy.distance

def get_elevation_open_api(lat, lng):
    """
    Returns the elevation of a specific location on earth using open-elevation API.
    """

    ## build the url for the API call
    ELEVATION_BASE_URL = 'https://api.open-elevation.com/api/v1/lookup'
    URL_PARAMS = "locations=%.7f,%.7f" % (lat, lng)
    url = ELEVATION_BASE_URL + "?" + URL_PARAMS

    ## make the call (ie. read the contents of the generated url) and decode the
    ## result (note: the result is in json format).
    with urllib.request.urlopen(url) as f:
        response = json.loads(f.read().decode())

    result = response["results"][0]
    elevation = float(result["elevation"])
    lat = float(result["latitude"])
    lng = float(result["longitude"])
        
    return (elevation, lat, lng)


# load mini DB of elevations

elevations_file = 'nodes_elevation.csv'
df_elevations = pd.read_csv(elevations_file)
data_elevations = df_elevations.to_dict('records')

def closest_point(data, v):
    return min(data, key=lambda p: geopy.distance.vincenty(v['lat'],v['lon'],p['lat'],p['lon']).m)


def get_elevation_offline(lat, lon):
    v = {'lat': lat, 'lon': lon}
    return closest_point(data_elevations, v)


def calculate_ski_route(dst_lat, dst_lon, src_lat, src_lon):
    return {'test': 'true'}