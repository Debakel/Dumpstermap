"""Converts a GeoJSON-like representation of geospatial data to KML

Important
---------
The `properties` of a GeoJSON-like feature can be an arbitrary JSON object, whereas with KML there is a fixed set of properties (namely
`name` and `description`).
If the GeoJSON dataset contains properties other than `name` and `description`, they will be ignored.
Consider transforming the GeoJSON dataset to a schema compatible with KML before conversion.
"""
from tempfile import NamedTemporaryFile

import fiona
import geopandas

from tokml.types import GeoFeature

__all__ = ["to_file", "to_string"]

# Enable KML support which is disabled by default
fiona.drvsupport.supported_drivers["KML"] = "rw"


def to_file(features: GeoFeature, filename: str):
    """Saves the given geospatial features to a KML file.

    Parameters
    ----------
        features
            - Iterable of features, where each element must be a feature
              dictionary or implement the __geo_interface__.
            - Feature collection, where the 'features' key contains an
              iterable of features.
            - Object holding a feature collection that implements the
              ``__geo_interface__``.
        filename
            File path to write to.
    """

    geodata_frame = geopandas.GeoDataFrame.from_features(features)
    geodata_frame.to_file(filename, driver="KML", engine="fiona")


def to_string(features: GeoFeature, folder_name: str = "Places") -> str:
    """Converts the given geospatial features to a KML string.

    Parameters
    ----------
        features
            See ``tokml.to_file`` for details.
        folder_name
            Name of the KML folder to place the features in.
    """
    tmp_file = NamedTemporaryFile(mode="w+", prefix=f"{folder_name}.kml")
    to_file(features, tmp_file.name)
    return tmp_file.read()
