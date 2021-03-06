from flask import Flask, jsonify, request
import json
from flask_cors import CORS
import geopy.distance
from hta_utils import *
from scipy.spatial import distance
from parser import *

app = Flask(__name__)
CORS(app)


# load mini DB of locations
locations_file = 'gast.json'
with open(locations_file) as f:
    db_locations = json.load(f)


# show locations with distance from the viewpoint
@app.route('/locations')
def get_locations():
    locations_res = db_locations['List']
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    my_coords = (lat, lon)

    for item in locations_res:
        to_coords = (item['Latitude'], item['Longitude'])
        item['Distance'] = geopy.distance.vincenty(to_coords, my_coords).m
        
    return jsonify(locations_res)


@app.route('/skiroute')
def get_skiroute():
    src_lat = float(request.args.get('src_lat'))
    src_lon = float(request.args.get('src_lon'))
    dst_lat = float(request.args.get('dst_lat'))
    dst_lon = float(request.args.get('dst_lon'))
    route = calculate_ski_route(dst_lat, dst_lon, src_lat, src_lon)

    src_elv = get_elevation_offline(src_lat, src_lon)
    dst_elv = get_elevation_offline(dst_lat, dst_lon)

    dist_2d = geopy.distance.vincenty((dst_lat, dst_lon), (src_lat, src_lon)).m # test

    a = (0, 0)
    elv_diff = dst_elv['elevation'] - src_elv['elevation']
    b = (dist_2d, elv_diff)
    route['TotalDistance'] = int(distance.euclidean(a, b))
    route['TotalDistanceText'] = str(route['TotalDistance']) + " meters"
    route['TimeInSeconds'] = int(route['TotalDistance'] / NOVICE_AVG_SKIING_SPEED)
    route['TimeInText'] = display_time(route['TimeInSeconds'])
    route['ElevationDiff'] = abs(int(elv_diff))
    route['ElevationDiffText'] = str(route['ElevationDiff']) + " meters"
    route['VerticalDirection'] = "Down" if dst_elv['elevation'] < src_elv['elevation'] else "Up"
    route['VerticalDirectionText'] = "Going " + route['VerticalDirection']

    return jsonify(route)


@app.route('/skiroute_extra')
def get_skiroute_extra():
    src_lat = float(request.args.get('src_lat'))
    src_lon = float(request.args.get('src_lon'))
    dst_lat = float(request.args.get('dst_lat'))
    dst_lon = float(request.args.get('dst_lon'))

    route = {}
    route['Way'] = way_to_interest_point((src_lat, src_lon), (dst_lat, dst_lon))

    return jsonify(route)


if __name__ == "__main__":
    app.run(port=5000)