"""Management command to publish all locations as a KML file to a S3 bucket.

Configuration
-------------

AWS credentials must be provided either via the credentials file located at `~/.aws/credentials` (see
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) or via environment variables:

`.env`:
```
AWS_ACCESS_KEY_ID=      # required
AWS_SECRET_ACCESS_KEY=  # required
AWS_DEFAULT_REGION=     # optional
AWS_ENDPOINT_URL=       # optional
KML_EXPORT_BUCKET_NAME= # required
```

"""
import datetime
import logging
from typing import Iterable

import bucketstore
from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

from dumpsters.models import Dumpster


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Export all locations to a KML string
        kml = locations_to_kml(Dumpster.objects.all())

        # Publish KML export to S3 bucket
        bucket = bucketstore.get(settings.KML_EXPORT_BUCKET_NAME)

        s3_key: bucketstore.S3Key = bucket.key("dumpsters.kml")
        s3_key.set(kml)
        s3_key.make_public()

        logging.info("Locations published to %s" % s3_key.url)


def locations_to_kml(locations: Iterable[Dumpster]) -> str:
    places = [
        {
            "name": location.name,
            "description": description(location),
            "kml": location.location.kml,
        }
        for location in locations
    ]
    return render_to_string("gis/kml/placemarks.kml", {"places": places})


def description(location: Dumpster) -> str:
    return (
        f"Data exported from Dumpstermap.org on {datetime.date.today().isoformat()}"
        "\n\n\n"
        f"More info on https://www.dumpstermap.org/detail/{location.id}"
    )
