import csv
from trashmap.DB import Store
from trashmap.Model import OSMNode, Dumpster, Vote, Comment
from ConfigParser import ConfigParser

config = ConfigParser()
config.read('trashmap/trashmap.config')

# Get Database
store = Store(config.get('Database', 'connection'))
session = store.session


def filter_csv_file(input, output):
    fin = open(input, 'r')
    fout = open(output, 'w')
    writer = csv.writer(fout, delimiter=',')
    for row in csv.reader(fin, delimiter=','):
        if row[1] == '2':
            writer.writerow(row)
            lat = row[2]
            long = row[3]
            id = int('99' + str(row[0]))  # 99 <fallingfruit-id>
            if store.get(OSMNode, id=id) is None:
                osmnode = OSMNode(id=id, location='POINT(' + str(long) + ' ' + str(lat) + ')')
                dumpster = Dumpster(osmnode=osmnode)
                voting = Vote(dumpster=dumpster, value=5)
                comment = Comment(dumpster=dumpster, name="Fallingfruits.org", comment=row[5])
                store.session.add(osmnode)
                store.session.add(dumpster)
                store.session.add(voting)
                store.session.add(comment)
                store.session.commit()


filter_csv_file("/home/m/SE/Trashmap/data/fallingfruits/locations.csv",
                "/home/m/SE/Trashmap/data/fallingfruits/filtered.csv")
