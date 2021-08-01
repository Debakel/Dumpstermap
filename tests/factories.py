import datetime

import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime

from dumpsters.models import Dumpster
from tests.providers import GeoPointProvider

factory.Faker.add_provider(GeoPointProvider)


class DumpsterFactory(DjangoModelFactory):
    class Meta:
        model = Dumpster

    location = factory.Faker('point')
    created = FuzzyDateTime(datetime.datetime(2008, 1, 1, tzinfo=datetime.timezone.utc))
