import tokml


def test_tokml() -> None:
    assert kml_string == tokml.to_string(geojson_dict)


geojson_dict = {
    "type": "FeatureCollection",
    "features": [
        {
            "id": 1,
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-3.7349187842251217, 56.7042560452053],
            },
            "properties": {
                "name": "The Plaice to Be",
                "description": "Traditional fish & chips, and more, all cooked to order.",
            },
        },
        {
            "id": 2,
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [-10.0, 50.5]},
            "properties": {
                "name": "Another place",
                "description": "Lorem Ipsum",
            },
        },
    ],
}
kml_string = """<?xml version="1.0" encoding="utf-8" ?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document id="root_doc">
<Folder><name>Places</name>
  <Placemark>
	<name>The Plaice to Be</name>
	<description>Traditional fish &amp; chips, and more, all cooked to order.</description>
      <Point><coordinates>-3.73491878422512,56.7042560452053</coordinates></Point>
  </Placemark>
  <Placemark>
	<name>Another place</name>
	<description>Lorem Ipsum</description>
      <Point><coordinates>-10,50.5</coordinates></Point>
  </Placemark>
</Folder>
</Document></kml>
"""
