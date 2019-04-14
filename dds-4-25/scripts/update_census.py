import sys
import random

from pymongo import MongoClient


if len(sys.argv) != 3:
    print "Usage: ", sys.argv[0], "<filename> <MongoDB database name>"
    exit(1)

filename = sys.argv[1]
records = []
uri = "mongodb://127.0.0.1:27017/"
client = MongoClient(uri + sys.argv[2])
db = client[sys.argv[2]]
collection = db.companies

print "Opening", filename

with open(filename, 'r') as f:
    for line in f:
        if not len(records) % 10000:
            print len(records), "records parsed"
        #if len(records) >= 10000: break
        records.append([value.strip() for value in line.split('\t')])

colnames = records.pop(0)

print "Finished parsing", len(records), "records"
print "Column headers:",
for colname in colnames: print colname,


def printrecord(record):
    for j, colname in enumerate(colnames):
        print colname + ":",
        print record[j]
    print


def record_dict(record):
    return dict(z for z in zip(colnames, [v.decode('latin-1') for v in record]) if z[1])


print "\n\nSample records:\n"

printrecord(random.choice(records))
printrecord(random.choice(records))

if raw_input("Are these records sensibly parsed? (y/n) ") != "y":
    print "Aborting"
    exit(1)

print "\nSample serialized records:\n"
print record_dict(random.choice(records))
print record_dict(random.choice(records))

if raw_input("\nAre these records sensibly serialized? (y/n) ") != "y":
    print "Aborting"
    exit(1)

if raw_input("Is this correct? (y/n) ") != 'y':
    print "Aborting"
    exit(1)

totalsize = sum([sys.getsizeof(record) for record in records])
print "Upload", len(records), "records and approximately ", totalsize, "bytes? (y/n)",
if raw_input() != 'y':
    print "Aborting"
    exit(1)

b = []
names = []
for i, record in enumerate(records):
    b.append(record_dict(record))
    if i and not i % 1000:
        print "Uploading 10000 records"
        collection.insert(b)
        b = []
        print "Uploaded", i, "records so far"

if b: collection.insert(b)
print "Upload succeeded"
