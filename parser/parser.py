from imposm.parser import OSMParser
from geopy.geocoders import Nominatim
import json
from geopy.distance import geodesic
from pprint import pprint

geolocator = Nominatim(user_agent="hackthealps")
with open('data/gast.json') as f:
    data = json.load(f)

restaurants = {}
for dict in data['List']:
    for key in dict:
        restaurants[dict["Name"]] = {"Latitude":dict["Latitude"], "Longitude":dict["Longitude"], "Altitude":dict["Altitude"]}

stationlist = []
pistedict = {}
coordslist = []

def ways_callback(ways):
    # callback method for ways
    for osmid, tags, refs in ways:
        for tag in tags:
            if tag == "piste:difficulty" and "piste:ref" in tags or "piste:number" in tags:
                if str(tags[tag]) in pistedict:
                    pistedict[str(tags[tag])].append({"tags":tags, "refs":refs})
                else:
                    pistedict[str(tags[tag])] = [{"tags":tags, "refs":refs}]
def coords_callback(coords):
    global coordslist
    coordslist = coords

p = OSMParser(concurrency=4, ways_callback=ways_callback, coords_callback=coords_callback)
p.parse('data/kronplatz.osm')



def cmp_items(a, b):
    if a["dist"] > b["dist"]:
        return 1
    elif a["dist"] == b["dist"]:
        return 0
    else:
        return -1


def find_piste_by_category(coords, piste_list = None):
    min_distance = 10000
    min_pist = None
    closest_node = None
    coords = None


    for piste in piste_list:
        for node in coordslist:
            dist = geodesic(coords, (node[2], node[1])).kilometers
            piste["dist"] = dist
            if node[0] in piste["refs"]:
                if min_distance > dist:
                    min_distance = dist
                    coords = (node[2], node[1])
                    closest_node = node[0]
                    min_pist = piste
        # print piste
    piste_list.sort(cmp=cmp_items)
    # return piste_list
    return (min_pist, min_distance, coords, closest_node)


def find_start_to_piste(coords):
    easy_piste = find_piste_by_category(coords, pistedict["easy"])
    intermediate_piste = find_piste_by_category(coords, pistedict["intermediate"])
    advanced_piste = find_piste_by_category(coords, pistedict["advanced"])

    return {"easy":easy_piste,"intermediate":intermediate_piste, "advanced":advanced_piste}

def find_piste_to_interest_point(piste, end):
    return None

def way_to_interest_point(start, end, preferences=None):
    piste_start_options = find_start_to_piste(start)
    piste_end_options = find_start_to_piste(end)

    print piste_start_options

    return {"way_id":None, "coords":None, "distance":None}

way_to_interest_point((46.738097,11.957705), (46.7403845,11.9567158))