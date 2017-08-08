#!/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.objects import *
import datetime as dt
import argparse
import pandas


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Submit samples')
    parser.add_argument('--delim', default=',', help='CSV delimiter [,]')
    parser.add_argument('-f', '--format', default='csv', choices=['csv', 'excel'], help='Table format [csv]')
    parser.add_argument('table', help='Sample table')
    args = parser.parse_args()

    if args.format == 'csv':
        table = pandas.read_csv(args.table, sep=args.delim)
    elif args.format == 'excel':
        table = pandas.read_excel(args.table)
    else:
        raise RuntimeError('unknown table format')

    print table

    engine = create_engine('sqlite:///testdb')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    for ix, row in table.iterrows():
        try:
            smpl = Sample.make(row.sample_type, row.to_dict())
            session.add(smpl)
        except Exception as e:
            print e.message

    session.commit()
