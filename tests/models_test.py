from dumpsters.models import Dumpster


def test_geo_interface():
    """Ensure the dumpster model correctly implements the __geo_interface__ protocol."""
    dumpster = Dumpster(id=1, location="POINT(1 1)", name="REWE")
    assert dumpster.__geo_interface__ == {
        "geometry": {"coordinates": [1.0, 1.0], "type": "Point"},
        "properties": {"id": 1, "name": "REWE"},
        "type": "Feature",
    }
