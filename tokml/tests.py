import os
from string import Template
from tempfile import NamedTemporaryFile

import tokml


def test_to_file():
    """Ensure exporting a GeoJSON object to a KML file works"""
    # GIVEN
    file = NamedTemporaryFile(suffix=".kml", mode="r")

    # WHEN
    tokml.to_file(geojson_dict, file.name)

    # THEN
    content = file.read()
    kml_folder_name = os.path.basename(file.name).split(".kml")[0]
    assert content == expected_kml_string.substitute(name=kml_folder_name)


def test_to_string():
    """Ensure exporting a GeoJSON object to a KML string works"""
    assert "<name>The Plaice to Be</name>" in tokml.to_string(geojson_dict)
    assert expected_kml_string.substitute(name="Lorem Ipsum") == tokml.to_string(
        geojson_dict, folder_name="Lorem Ipsum"
    )


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
expected_kml_string = Template(
    """<?xml version="1.0" encoding="utf-8" ?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document id="root_doc">
<Folder><name>$name</name>
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
)
