from rest_framework import status
from rest_framework.test import APIClient

from tests.factories import DumpsterFactory


def test_dumpsters_list(db):
    dumpster = DumpsterFactory()

    response = APIClient().get('/dumpsters/')

    assert response.status_code == status.HTTP_200_OK

    assert response.data["type"] == "FeatureCollection"
    assert len(response.data["features"]) == 1
    assert response.data["features"][0]["id"] == dumpster.id
