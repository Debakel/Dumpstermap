__author__ = 'niemand'

from DB import Store
from Model import *
from geoalchemy2.shape import to_shape
from geojson import Point, Feature, FeatureCollection
import json

# Get Database
store = Store()
session = store.session

def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data
def import_geojson(filename):
    data = read_json(filename)
    for feature in data['features']:
        osm_id = int(feature['id'].replace("node/", ""))
        if 'name' in feature['properties']:
            name = feature['properties']['name']
        else:
            name = ""
        long    = feature['geometry']['coordinates'][0]
        lat     = feature['geometry']['coordinates'][1]
        print "ID: " + str(osm_id) + " Name: " + name + " long: " + str(long) + " lat: " + str(lat)

        # Insert into Database
        node = OSMNode(osm_id=osm_id, name=name, location='POINT('+str(long) + ' ' + str(lat) + ')')
        session.add(node)
        session.commit()
def create_dumpster_for_all_osmnodes():
    osmnodes = session.query(OSMNode).all()
    for osmnode in osmnodes:
        if not store.exists(Dumpster, osmnode=osmnode):
            new_dumpster = Dumpster(osmnode=osmnode)
            session.add(new_dumpster)
            session.commit()
#import_geojson('data/shop_augsburg.geojson')
create_dumpster_for_all_osmnodes()