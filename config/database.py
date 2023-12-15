import os

from sqlalchemy import create_engine, event
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


sqlite_file_name = '../database.sqlite'
base_dir = os.path.dirname(os.path.realpath(__file__))
database_uri = 'sqlite:///' + os.path.join(base_dir, sqlite_file_name)

engine = create_engine(database_uri, echo=True)

event.listen(engine, 'connect', lambda conn, rec: conn.execute('pragma foreign_keys=ON'))

SessionDB = sessionmaker(bind=engine)
Base = declarative_base()