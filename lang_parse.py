import csv
import os 
def parse():
    values = {}
    with open(os.path.join('lookups','langs.csv'), 'r', newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for i in range(len(header)-1):
            values[header[i+1]]={}
        for row in reader:
            ref = row[0]
            for i in range(len(row)-1):
                values[header[i+1]][ref]=row[i+1]
    return values
