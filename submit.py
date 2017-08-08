#!/bin/env python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.objects import *
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
        raise RuntimeError('unknown table format [{}]'.format(args.format))

    print table

    # set up an sql file-based database
    engine = create_engine('sqlite:///testdb', echo=True)
    Base.metadata.create_all(engine)

    # open a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # currently this will duplicate instances. We need to read further on object identity
    # handling within sqlalchemy.
    for ix, row in table.iterrows():
        try:
            smpl = Sample.make(row.sample_class, row.to_dict())
            session.add(smpl)
        except Exception as e:
            print e.message

    # commit our changes
    session.commit()

    # pull all rows from the database
    for n, s in enumerate(session.query(Sample).all(), start=1):
        print n, s.id, s.name
