from flask import Flask, request
from Model import Dumpster, Vote, Comment, OSMNode
from DB import Store
from geojson import FeatureCollection, Feature
from ConfigParser import ConfigParser
import json
import Geo
from pprint import pprint
from shapely.geometry import Polygon, Point
from shapely.wkt import dumps, loads
from sqlalchemy import func

config = ConfigParser()
if __name__ == '__main__':
    config.read('trashmap.config')
else:
    config.read('trashmap/trashmap.config')

app = Flask(__name__)

store = Store(config.get('Database', 'connection'))
session = store.session

@app.route('/')
def map():
    return app.send_static_file('app.html')

##
## Votes
##
@app.route('/api/vote/<int:dumpster_id>/<string:vote>')
def vote(dumpster_id, vote):
    dumpster = store.get(Dumpster, id=dumpster_id)
    if dumpster is None:
        return json.dumps({'success': False})
    elif not (vote is 'up' or 'down'):
        return json.dumps({'success': False, 'reason': "vote must be 'up' or 'down'"})
    else:
        if vote == 'up':
            value = 1
        elif vote == 'down':
            value = -1
        new_vote = Vote(dumpster=dumpster, value=value)
        store.session.add(new_vote)
        store.session.commit()
    return json.dumps({'success': True})


##
## Dumpster
##
@app.route("/api/dumpster/all")
def all_dumpsters():
    dumpsters = store.get_all(Dumpster)
    features = []
    for dumpster in dumpsters:
        features.append(dumpster.__geojson__())
    featurecollection = FeatureCollection(features)
    return str(featurecollection)


def get_osmnodes_in_tile(zoom, x, y):
    # See https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames for documentation about slippy maps and how to convert Tile numbers to lon./lat.
    lat_top, lng_left = Geo.tilenum2deg(x, y, zoom)
    lat_bottom, lng_right = Geo.tilenum2deg(x + 1, y + 1, zoom)
    boundary = Polygon([(lng_left, lat_top), (lng_right, lat_top), (lng_right, lat_bottom), (lng_left, lat_bottom)])
    boundary_wkt = dumps(boundary)
    query = store.session.query(OSMNode).filter(
            func.ST_Contains(boundary_wkt, OSMNode.location))
    return query.all()


def filter_osmnodes_by_voting(osmnodes, voting):
    # todo: filter by sql query
    voting = str(voting)
    good = []
    bad = []
    neutral = []
    for osmnode in osmnodes:
        dumpster = osmnode.dumpster
        if dumpster.voting < 0:
            bad.append(dumpster.osmnode)
        elif dumpster.voting > 0:
            good.append(dumpster.osmnode)
        elif dumpster.voting == 0:
            neutral.append(dumpster.osmnode)

    if voting == "good":
        return good
    elif voting == "bad":
        return bad
    elif voting == "neutral":
        return neutral
    else:
        raise Exception()


@app.route("/api/dumpster/tiles/clustered/<int:zoom>/<int:x>/<int:y>")
def dumpster_tiles_cluster(zoom, x, y):
    if zoom < 12:
        query = get_osmnodes_in_tile(zoom, x, y)
        count = query.count()
        if count >= 1:
            lat, lng = Geo.tilenum2deg(x + 0.5, y + 0.5, zoom)
            cluster_point = Point(lng, lat)
            feature_collection = FeatureCollection([Feature(geometry=cluster_point, properties=[])])
            return str(feature_collection)

    return "{}"


def test():
    # todo: remove!
    query = store.session.query(OSMNode)
    c = query.count()
    query2 = query.filter_by(OSMNode.dumpster.voting > 0)
    c2 = query2.count()
    a = query.all()
    i = 1 + 1


@app.route("/api/dumpster/tiles/<int:zoom>/<int:x>/<int:y>/<voting>")
@app.route("/api/dumpster/tiles/<int:zoom>/<int:x>/<int:y>")
def dumpster_tiles(zoom, x, y, voting=None):
    query = get_osmnodes_in_tile(zoom, x, y)
    if voting is not None:
        query = filter_osmnodes_by_voting(query, voting)
    features = []
    # features.append(Feature(geometry=boundary))  # adds tile polygon (usefull while debugging)
    for node in query:
        dumpster = node.dumpster
        features.append(dumpster.__geojson__())
    featurecollection = FeatureCollection(features)
    return str(featurecollection)

@app.route('/api/dumpster/<int:id>')
def dumpster(id):
    d = store.get(Dumpster, id=id)
    return str(d.__geojson__())


@app.route("/api/dumpster/good")
def good_dumpsters():
    dumpsters = store.get_all(Dumpster)
    features = []
    for dumpster in dumpsters:
        if dumpster.voting > 0:
            features.append(dumpster.__geojson__())
    featurecollection = FeatureCollection(features)
    return str(featurecollection)


## Comments
##

#
# POST: comment, name
#
@app.route('/api/comments/add/<int:dumpster_id>', methods=['POST'])
def add_comment(dumpster_id):
    dumpster = store.get(Dumpster, id=dumpster_id)
    if dumpster is None:
        result = json.dumps({'success': False, 'reason': str(id) + ' not known'})
        print result
        return result
    else:
        pprint(request.form)
        comment = request.form['comment']
        if 'name' in request.form and request.form['name'] != "":
            username = request.form['name']
        else:
            username = "Anonym"
        new_comment = Comment(dumpster=dumpster, name=username, comment=comment)
        store.session.add(new_comment)
        store.session.commit()
        result = json.dumps({'success': True})
        print result
        return result


if __name__ == '__main__':
    app.run(port=config.getint('Webserver', 'port'), debug=True)
