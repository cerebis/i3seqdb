from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Table

# orm base class
Base = declarative_base()




class Sample(Base):
    """
    Defined by the minimum required for submission at NCBI
    
    Subclasses are easily handled and one is included for clarity. These become a single
    table by default. Requirements such as non-null at the database level require individual
    tables -- supported by alchemy
    """
    @staticmethod
    def make(sample_type, kwargs):
        sample_type = sample_type.lower()
        if sample_type == 'microbe':
            return Microbe(**kwargs)
        else:
            raise RuntimeError('unknown sample type [{}]'.format(sample_type))

    __tablename__ = 'sample'

    id = Column(Integer, primary_key=True)

    name = Column(String)
    organism = Column(String)
    collection_date = Column(Date)
    geo_loc_name = Column(String)

    # simple one-to-many
    libraries = relationship('Library')


class Microbe(Sample):
    """
    Inheritence example. For this simple single-table case, no additional id is required
    """

    strain = Column(String)
    isolate = Column(String)
    host = Column(String)
    isolation_source = Column(String)
    sample_type = Column(String)


# many-to-many join tables

pool_library_table = Table('pool_library', Base.metadata,
                           Column('pool_id', Integer, ForeignKey('pool.id')),
                           Column('library_id', Integer, ForeignKey('library.id')))


class Library(Base):
    """
    A library should encompass all that there is to know about the creation of a sequencing library.
    What is required will depend on the library type, such as: amplicon, wgs, hic, meta3c
    """

    __tablename__ = 'library'

    id = Column(Integer, primary_key=True)

    # barcodes could be a separate table acting as an enumeration and tracking oligo batches.
    barcode = Column(String)
    creation_date = Column(Date)
    # status/step could be used to track process of creating library
    status = Column(String)
    tray = Column(String)
    well = Column(String)
    # bioanalyzer concentration
    ba_conc = Column(Float)
    # nano-run read count
    nano_count = Column(Integer)

    # foreign key of parent library
    sample_id = Column(Integer, ForeignKey('sample.id'))
    # many-to-many with pools
    pools = relationship('Pool', secondary=pool_library_table, back_populates='libraries')


run_pool_table = Table('run_pool', Base.metadata,
                       Column('run_id', Integer, ForeignKey('run.id')),
                       Column('pool_id', Integer, ForeignKey('pool.id')))


class Pool(Base):
    """
    A pool represents a combination of one or more libraries, before submitting as a run.
    """

    __tablename__ = 'pool'

    id = Column(Integer, primary_key=True)

    # some measure of concentration
    molarity = Column(Float)

    # many-to-many with library
    libraries = relationship('Library', secondary=pool_library_table, back_populates='pools')
    # many-to-many with run
    runs = relationship('Run', secondary=run_pool_table, back_populates='pools')


class Run(Base):
    """
    An actual sequencing run. This information would be populated at the time a run is handed
    to a sequencing facility, and would require updating once results are returned.
    """

    __tablename__ = 'run'

    id = Column(Integer, primary_key=True)

    facility = Column(String)
    machine_type = Column(String)
    cell_type = Column(String)  # redundant perhaps
    run_type = Column(String)
    run_date = Column(Date)
    data_path = Column(String)

    # many-to-many with pool
    pools = relationship('Pool', secondary=run_pool_table, back_populates='runs')