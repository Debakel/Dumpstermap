from freezegun import freeze_time

from dumpsters.management.commands.publish_kml import locations_to_kml
from dumpsters.models import Dumpster


@freeze_time("2023-12-24")
def test_locations_to_kml():
    """Ensure a list of dumpsters can be converted to a KML string."""
    dumpsters = [
        Dumpster(id=1, location="POINT(1 2)", name="REWE"),
        Dumpster(id=2, location="POINT(3 4)", name="Aldi & Co"),
    ]

    kml = locations_to_kml(dumpsters)

    assert (
        """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.1">
<Document>

  <Placemark>
    <name>REWE</name>
    <description>Data exported from Dumpstermap.org on 2023-12-24


More info on https://www.dumpstermap.org/detail/1</description>
    <Point><coordinates>1.0,2.0,0</coordinates></Point>
  </Placemark>
  <Placemark>
    <name>Aldi &amp; Co</name>
    <description>Data exported from Dumpstermap.org on 2023-12-24


More info on https://www.dumpstermap.org/detail/2</description>
    <Point><coordinates>3.0,4.0,0</coordinates></Point>
  </Placemark>
</Document>
</kml>
"""
        == kml
    )
