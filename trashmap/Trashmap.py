from flask import Flask, request
from Model import Dumpster, Vote, Comment
from DB import Store
from geojson import FeatureCollection
from ConfigParser import ConfigParser
import json
from pprint import pprint

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
    return json.dumps( {'success': True})


##
## Dumpster
##
@app.route("/api/dumpster/all")
def get_dumpsters():
    dumpsters = store.get_all(Dumpster)
    features = []
    for dumpster in dumpsters:
        features.append(dumpster.__geojson__())
    featurecollection = FeatureCollection(features)
    return str(featurecollection)


@app.route('/api/dumpster/<int:id>')
def get_dumpster(id):
    d = store.get(Dumpster, id=id)
    return str(d.__geojson__())


##
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
