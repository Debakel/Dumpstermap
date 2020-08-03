from django.core.management.base import BaseCommand, CommandError
import csv

from dumpsters.models import Dumpster, Voting

class Command(BaseCommand):
    help = 'Loads a fallingfruit.org data dump and extracts dumpster entries to a .csv file'

    def add_arguments(self, parser):
        parser.add_argument('--input', type=str)
        parser.add_argument('--output', type=str)

    def handle(self, *args, **options):
        TYPES = ['2', '836']
        ROW_COMMENT = 5
        IMPORTED_FROM = 'fallingfruit.org'

        input_filename = options['input']
        output_filename = options['output']
        input_file = open(input_filename)
        output_file = open(output_filename, 'w')

        print('Reading from {}.'.format(input_filename))

        csv_writer = csv.writer(output_file)
        csv_reader = csv.reader(input_file, delimiter=',')
        csv_writer.writerow(csv_reader.next()) # write header

        for row in csv_reader:
            if row[1] in TYPES: # type in first row; '2' is dumpster
                csv_writer.writerow(row)

        print('Finished.')

