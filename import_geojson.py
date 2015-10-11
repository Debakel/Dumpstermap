__author__ = 'niemand'

from trashmap.DB import Store
from trashmap.Model import *
from geoalchemy2.shape import to_shape
from geojson import Point, Feature, FeatureCollection
import json
from ConfigParser import ConfigParser
config = ConfigParser()
config.read('trashmap/trashmap.config')

# Get Database
store = Store(config.get('Database','connection'))
session = store.session

def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data
def import_geojson(filename):
    data = read_json(filename)
    for feature in data['features']:
        osm_id = int(feature['id'].replace("node/", ""))
        properties = feature['properties']
        geometry = feature['geometry']

        long    = geometry['coordinates'][0]
        lat     = geometry['coordinates'][1]
        print "ID: " + str(osm_id)  + " long: " + str(long) + " lat: " + str(lat)

        # Create node
        node = OSMNode(osm_id=osm_id, location='POINT('+str(long) + ' ' + str(lat) + ')')
        if 'name' in properties:
            node.name = properties['name']
        if 'addr:street' in properties:
            node.street = properties['addr:street']
        if 'addr:housenumber' in properties:
            node.housenumber = properties['addr:housenumber']
        if 'addr:city' in properties:
            node.city = properties['addr:city']

        # Insert in Database
        session.add(node)
        session.commit()
def create_dumpster_for_all_osmnodes():
    osmnodes = session.query(OSMNode).all()
    for osmnode in osmnodes:
        if not store.exists(Dumpster, osmnode=osmnode):
            new_dumpster = Dumpster(osmnode=osmnode)
            session.add(new_dumpster)
            session.commit()
import_geojson('data/shop_augsburg.geojson')
#create_dumpster_for_all_osmnodes()