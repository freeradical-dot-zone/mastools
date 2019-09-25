"""Common database things used everywhere."""

from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


@lru_cache()
def session_for(*, host, database, user, password, port=5432):
    """Return a (possibly cached) session for the connection details."""

    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
    engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
