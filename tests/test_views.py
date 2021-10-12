from rest_framework import status
from rest_framework.test import APIClient

from dumpsters.models import Dumpster, Voting
from tests.factories import DumpsterFactory


def test_dumpsters_list(db):
    dumpster = DumpsterFactory()

    response = APIClient().get('/dumpsters/')

    assert response.status_code == status.HTTP_200_OK

    assert response.data["type"] == "FeatureCollection"
    assert len(response.data["features"]) == 1
    assert response.data["features"][0]["id"] == dumpster.id


def test_dumpsters_tile_view(db):
    dumpster1 = DumpsterFactory(location='POINT(-1 -1)')
    dumpster2 = DumpsterFactory(location='POINT(0 0)')

    response = APIClient().get('/dumpsters/tiles/2/1/2/')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['features']) == 1
    assert response.data["features"][0]["id"] == dumpster1.id


def test_dumpsters_create(db):
    url = '/dumpsters/'
    data = {"type": "Feature", "geometry": {"type": "Point", "coordinates": [1, 1]},
            "properties": {"name": "REWE", "voting_set": [{"value": "good", "comment": "Hallo123"}]}}

    response = APIClient().post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED

    assert Dumpster.objects.count() == 1
    assert Dumpster.objects.filter(name='REWE', voting__value='good', voting__comment="Hallo123").exists()

    assert response.data['properties']['name'] == 'REWE'


def test_votings_create(db):
    dumpster: Dumpster = DumpsterFactory()

    url = '/votings/'
    data = {"dumpster": dumpster.id, "value": "good", "comment": "Hallo123", "user": {}}

    response = APIClient().post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED

    assert Voting.objects.filter(dumpster=dumpster, value="good", comment="Hallo123").exists()

    assert response.data['dumpster'] == dumpster.id
    assert response.data['comment'] == "Hallo123"
    assert response.data['value'] == 'good'
