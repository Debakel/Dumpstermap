"""Management command to publish all locations as a KML file to a S3 bucket.

AWS credentials must be provided either via the credentials file located at `~/.aws/credentials` (see
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) or via environment variables (`AWS_ACCESS_KEY_ID`,
`AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`).

Additionally, the name of the target S3 bucket must be defined in the `KML_EXPORT_BUCKET_NAME` environment variable.
"""
import logging
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

        logging.info("Locations published to %s" % s3_key.url)


def to_kml(locations: Iterable[Dumpster]) -> str:
    locations = [location.__geo_interface__ for location in locations]
    for dumpster in locations:
        identifier = dumpster["properties"].pop("id")
        dumpster["properties"][
            "description"
        ] = f"More info on https://www.dumpstermap.org/detail/{identifier}"

    kml = tokml.to_string(locations)

    return kml
