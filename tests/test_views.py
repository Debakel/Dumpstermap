from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APIClient

from dumpsters.models import Dumpster, Voting, VotingValue
from tests.factories import DumpsterFactory


def test_dumpsters_list(db):
    # GIVEN
    with freeze_time("2000-01-01"):
        dumpster = Dumpster.objects.create(location="POINT(1 2)")

    # WHEN
    response = APIClient().get("/dumpsters/")

    # THEN
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "type": "FeatureCollection",
        "features": [
            {
                "id": dumpster.id,
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [1.0, 2.0]},
                "properties": {
                    "name": "Dumpster",
                    "created": "2000-01-01T00:00:00Z",
                    "rating": 0,
                    "good": 0,
                    "bad": 0,
                    "voting_set": [],
                },
            }
        ],
    }


def test_dumpsters_tile_view(db):
    # GIVEN
    dumpster1 = DumpsterFactory(location="POINT(-1 -1)")
    dumpster2 = DumpsterFactory(location="POINT(0 0)")

    # WHEN
    response = APIClient().get("/dumpsters/tiles/2/1/2/")

    # THEN
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["features"]) == 1
    assert response.data["features"][0]["id"] == dumpster1.id


def test_dumpsters_within_bound(db):
    """Ensure filtering entries by bounding box works

    ▲
    │
    │   ┌──────────┐
    │   │          │
    │   │    p1    │
    │   │          │
    │   └──────────┘
    │
    │ p2
    └──────────────────────►
    """
    # GIVEN
    with freeze_time("2000-01-01"):
        dumpster1 = DumpsterFactory(location="POINT(1 1)")
    dumpster2 = DumpsterFactory(location="POINT(0.2 0.2)")

    # WHEN
    response = APIClient().get("/dumpsters/withinbounds/0.5/0.5/1.5/1.5/")

    # THEN
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "type": "FeatureCollection",
        "features": [
            {
                "id": dumpster1.id,
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [1.0, 1.0]},
                "properties": {"name": "Dumpster", "created": "2000-01-01T00:00:00Z"},
            }
        ],
    }


def test_dumpsters_count_within_bounds(db):
    # GIVEN - two spots within the bounding box; one outside
    DumpsterFactory(location="POINT(1 1)")
    DumpsterFactory(location="POINT(1.2 1.2)")
    DumpsterFactory(location="POINT(0.2 0.2)")  # <- outside the bbox

    # WHEN
    response = APIClient().get("/dumpsters/countwithinbounds/0.5/0.5/1.5/1.5/")

    # THEN
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"count": 2}


def test_dumpsters_count_within_bounds_empty(db):
    # GIVEN - no spots within the bounding box
    DumpsterFactory(location="POINT(5 5)")

    # WHEN
    response = APIClient().get("/dumpsters/countwithinbounds/0/0/1/1/")

    # THEN
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"count": 0}


def test_dumpsters_create(db):
    # GIVEN
    url = "/dumpsters/"
    data = {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [1, 1]},
        "properties": {
            "name": "REWE",
            "voting_set": [{"value": "good", "comment": "Hallo123"}],
        },
    }

    # WHEN
    with freeze_time("2000-01-01"):
        response = APIClient().post(url, data, format="json")

    # THEN
    assert response.status_code == status.HTTP_201_CREATED

    assert Dumpster.objects.count() == 1
    assert Voting.objects.count() == 1

    dumpster = Dumpster.objects.get(name="REWE")
    voting = dumpster.voting_set.first()
    assert response.data == {
        "id": dumpster.id,
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [1.0, 1.0]},
        "properties": {
            "name": "REWE",
            "created": "2000-01-01T00:00:00Z",
            "rating": 1,
            "good": 1,
            "bad": 0,
            "voting_set": [
                {
                    "id": voting.id,
                    "value": "good",
                    "comment": "Hallo123",
                    "created_date": "2000-01-01T00:00:00Z",
                    "name": "Anonymous",
                }
            ],
        },
    }


def test_votings_create(db):
    # GIVEN
    dumpster: Dumpster = DumpsterFactory()

    url = "/votings/"
    data = {"dumpster": dumpster.id, "value": "good", "comment": "Hallo123", "user": {}}

    # WHEN
    with freeze_time("2000-01-01"):
        response = APIClient().post(url, data, format="json")

    # THEN
    assert response.status_code == status.HTTP_201_CREATED

    voting = Voting.objects.get(
        dumpster=dumpster, value=VotingValue.GOOD, comment="Hallo123"
    )
    assert response.data == {
        "id": voting.id,
        "value": "good",
        "comment": "Hallo123",
        "created_date": "2000-01-01T00:00:00Z",
        "dumpster": dumpster.id,
        "name": "Anonymous",
    }


def test_root_redirects_to_dumpstermap_org(db):
    response = APIClient().get("/")

    assert response.status_code == status.HTTP_302_FOUND
    assert response["Location"] == "https://dumpstermap.org"
