from flask import Flask, jsonify, request
import json
from flask_cors import CORS
import geopy.distance
from hta_utils import *

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
    src_lat = request.args.get('src_lat')
    src_lon = request.args.get('src_lon')
    dst_lat = request.args.get('dst_lat')
    dst_lon = request.args.get('dst_lon')
    route = calculate_ski_route(dst_lat, dst_lon, src_lat, src_lon)

    #

    return jsonify(route)

if __name__ == "__main__":
    app.run(port=5001)