from datetime import datetime

import fastkml
import pytz
import requests
from django.core.management.base import BaseCommand

from dumpsters.models import Dumpster, Voting

map_url = "https://goo.gl/maps/8yvnAyv6wnHraoJ68"
kml_url = (
    "https://www.google.com/maps/d/kml?forcekml=1&mid=17Xuf9-ifgbGgnAUar-QcEcu4wG7o-s3O"
)


class Command(BaseCommand):
    help = "Imports locations from a Google Maps KML dump"

    def handle(self, *args, **options):
        content = requests.get(kml_url).content

        kml = fastkml.kml.KML()
        kml.from_string(content)

        features = list(kml.features())
        folders = list(features[0].features())

        for folder in folders:
            for feature in list(folder.features()):
                dumpster = Dumpster.objects.create(
                    name=feature.name,
                    location=feature.geometry.to_wkt(),
                    imported_from=map_url,
                    imported=True,
                )
                Voting.objects.create(
                    dumpster=dumpster,
                    value=Voting.GOOD,
                    comment=f"Copied from {map_url}",
                    created_date=datetime.now(pytz.utc),
                )
