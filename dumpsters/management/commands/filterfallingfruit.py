import csv

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Loads a fallingfruit.org data dump and extracts dumpster entries to a .csv file"

    def add_arguments(self, parser):
        parser.add_argument("--input", type=str)
        parser.add_argument("--output", type=str)

    def handle(self, *args, **options):
        TYPES = ["2", "836"]

        input_filename = options["input"]
        output_filename = options["output"]

        print(f"Reading from {input_filename}.")

        with (
            open(input_filename) as input_file,
            open(output_filename, "w") as output_file,
        ):
            csv_writer = csv.writer(output_file)
            csv_reader = csv.reader(input_file, delimiter=",")
            csv_writer.writerow(next(csv_reader))  # write header

            for row in csv_reader:
                if row[1] in TYPES:  # type in first row; '2' is dumpster
                    csv_writer.writerow(row)

        print("Finished.")
