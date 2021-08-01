import faker
from django.contrib.gis.geos import Point
from faker.providers import BaseProvider


class GeoPointProvider(BaseProvider):
    def point(self) -> Point:
        fake = faker.Faker()
        coords = fake.local_latlng()
        return Point(x=float(coords[1]), y=float(coords[0]), srid=4326)
