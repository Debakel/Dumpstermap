from typing import TypeVar, Union, Iterable, Protocol

from geojson import Feature, FeatureCollection


class GeoInterface(Protocol):
    """Protocol for objects that implement the __geo_interface__

    See https://gist.github.com/sgillies/2217756 for details.
    """

    __geo_interface__: dict


GeoFeature = TypeVar(
    "GeoFeature", bound=Union[Iterable[Feature], FeatureCollection, GeoInterface, dict]
)
