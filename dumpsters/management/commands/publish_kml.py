from typing import Iterable

import bucketstore
from django.conf import settings
from django.core.management.base import BaseCommand

from dumpsters.models import Dumpster
import tokml


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Export all locations to a KML string
        kml = to_kml(Dumpster.objects.all())

        # Publish KML export to S3 bucket
        bucket = bucketstore.get(settings.KML_EXPORT_BUCKET_NAME)

        s3_key: bucketstore.S3Key = bucket.key("dumpsters.kml")
        s3_key.set(kml)
        s3_key.make_public()


def to_kml(locations: Iterable[Dumpster]) -> str:
    locations = [location.__geo_interface__ for location in locations]
    for dumpster in locations:
        identifier = dumpster["properties"].pop("id")
        dumpster["properties"][
            "description"
        ] = f"More info on https://www.dumpstermap.org/detail/{identifier}"

    kml = tokml.to_string(locations)

    return kml
