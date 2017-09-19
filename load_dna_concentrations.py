#!/usr/bin/env python
import argparse
import pandas
import pymongo

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load DNA concentrations from a PicoGreen plate assay')
    parser.add_argument('table', help='Excel spreadsheet from plate reader')
    parser.add_argument('plate-id', help='ID of the plate')
    args = parser.parse_args()

    table = pandas.read_excel(args.table, encoding='ascii',skiprows=24,index_col=0,skip_footer=1)
    concs = table.as_matrix()

    client = MongoClient('mongodb://localhost:27017/')
    db = client.robolims_database
    plate = db.platemap.find_one({"plate_id": args.plate_id})
    for row in range(concs.shape[0]):
        for col in range(concs.shape[1]):
            sample_id = plate['wells'][row][col]
            sample = db.samples.find_one({"sample_id": sample_id})
            sample.concentration = concs[row,col]
            db.samples.update_one(sample)
