from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Table, CheckConstraint
import pandas


Base = declarative_base()


class Sample(Base):
    """
    Defined by the minimum required for submission at NCBI
    
    Subclasses are easily handled and one is included for clarity. These become a single
    table by default. Requirements such as non-null at the database level require individual
    tables -- supported by alchemy
    """
    __tablename__ = 'sample'

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False, unique=True)
    organism = Column(String, nullable=False)
    collection_date = Column(Date, nullable=False)
    geo_loc_name = Column(String, nullable=False)
    lat_lon = Column(String)
    _type= Column(String)

    # simple one-to-many
    libraries = relationship('Library')

    __mapper_args__ = {
        'polymorphic_identity': 'sample',
        'polymorphic_on': _type
    }

    @staticmethod
    def make(sample_class, kwargs):
        """
        Factory method for creating various subclasses of Sample.
        :param sample_class: the subclass to create
        :param kwargs: dict of fields, None/Nan fields will be removed.
        :return: instance of requested class
        """
        cl = sample_class.lower()

        # get rid of problematic elements before passing to constructor
        del kwargs['sample_class']
        for k in kwargs.keys():
            if not kwargs[k] or pandas.isnull(kwargs[k]):
                del kwargs[k]

        if cl == 'microbe':
            # this could be stored as a string and converted in the application
            # to a datetime instance
            return Microbe(**kwargs)
        elif cl == 'metagenome':
            return Metagenome(**kwargs)
        elif cl == 'pathogen':
            return Pathogen(**kwargs)
        else:
            raise RuntimeError('unknown sample type [{}]'.format(cl))



class Microbe(Sample):
    """
    Inheritence example. For this simple single-table case, no additional id is required
    """
    __tablename__ = 'microbe'

    id = Column(Integer, ForeignKey('sample.id'), primary_key=True)
    strain = Column(String)
    isolate = Column(String)
    host = Column(String)
    isolation_source = Column(String)
    sample_type = Column(String, nullable=False)

    __mapper_args__ = {'polymorphic_identity': 'microbe'}
    __table_args__ = (
        CheckConstraint('strain is not null or isolate is not null', name='check1'),
        CheckConstraint('host is not null or isolation_source is not null', name='check2'),
    )


class Pathogen(Sample):

    __tablename__ = 'pathogen'

    id = Column(Integer, ForeignKey('sample.id'), primary_key=True)
    strain = Column(String)
    isolate = Column(String)
    collected_by = Column(String)
    isolation_source = Column(String)

    __mapper_args__ = {'polymorphic_identity': 'pathogen'}
    __table_args__ = (
        CheckConstraint('strain is not null or isolate is not null', name='check1'),
    )

class Metagenome(Sample):

    __tablename__ = 'metagenome'

    id = Column(Integer, ForeignKey('sample.id'), primary_key=True)
    host = Column(String)
    isolation_source = Column(String)

    __mapper_args__ = {'polymorphic_identity': 'metagenome'}
    __table_args__ = (
        CheckConstraint('host is not null or isolation_source is not null', name='check1'),
    )

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