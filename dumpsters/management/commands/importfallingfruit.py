from django.core.management.base import BaseCommand

from dumpsters.models import Dumpster
from dumpsters.serializers import DumpsterSerializer


class Command(BaseCommand):
    help = "Exports dumpsters as geojson"

    def add_arguments(self, parser):
        parser.add_argument("file", nargs="+", type=str)

    def handle(self, *args, **options):
        filename = options["file"][1]
        dumpsters = Dumpster.objects.all()
        serializer = DumpsterSerializer(dumpsters, many=True)
        out = open(filename, "w")
        out.write(serializer.data)
        out.close()
