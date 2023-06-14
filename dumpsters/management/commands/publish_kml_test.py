from dumpsters.management.commands.publish_kml import locations_to_kml
from dumpsters.models import Dumpster


def test_dumpsters_to_kml():
    """Ensure a list of dumpsters can be converted to a KML string."""
    dumpsters = [
        Dumpster(id=1, location="POINT(1 1)", name="REWE"),
        Dumpster(id=2, location="POINT(1 1)", name="ALDI"),
    ]

    kml = locations_to_kml(dumpsters)

    assert (
        """<?xml version="1.0" encoding="utf-8" ?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document id="root_doc">
<Folder><name>Places</name>
  <Placemark>
	<name>REWE</name>
	<description>More info on https://www.dumpstermap.org/detail/1</description>
      <Point><coordinates>1,1</coordinates></Point>
  </Placemark>
  <Placemark>
	<name>ALDI</name>
	<description>More info on https://www.dumpstermap.org/detail/2</description>
      <Point><coordinates>1,1</coordinates></Point>
  </Placemark>
</Folder>
</Document></kml>
"""
        == kml
    )
