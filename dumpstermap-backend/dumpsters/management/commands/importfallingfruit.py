from django.core.management.base import BaseCommand, CommandError
import csv

from dumpsters.models import Dumpster, Voting

class Command(BaseCommand):
    help = 'Imports Dumpsters from fallings fruit .csv file'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        TYPE = '2'
        ROW_COMMENT = 5
        IMPORTED_FROM = 'fallingfruit.org'

        filename = options['file'][1]
        print('Importing from {}.'.format(filename))
        file = open(filename)
        count = 0
        for row in csv.reader(file, delimiter=','):
            if row[1] == TYPE: # type in first row; '2' is dumpster
                lat = row[2]
                long = row[3]
                id = str(row[0])

                if not Dumpster.objects.filter(imported_from = IMPORTED_FROM, import_reference=id).exists():
                    location ='POINT(' + str(long) + ' ' + str(lat) + ')'
                    dumpster = Dumpster(location=location, imported=True, imported_from=IMPORTED_FROM, import_reference=id)
                    dumpster.save()
                    voting = Voting(dumpster=dumpster, comment=row[ROW_COMMENT], value=Voting.GOOD)
                    voting.save()
                    count+=1

        print('Finished. Imported {} new objects.'.format(count))

