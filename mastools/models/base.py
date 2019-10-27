"""Common database things used everywhere."""

from functools import lru_cache

from psycopg2 import connect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # pylint: disable=invalid-name  ; This is an SQLAlchemy convention


@lru_cache()
def session_for(*, host, database, user, password, port=5432):
    """Return a (possibly cached) session for the connection details."""

    def pg_connect():
        """Return a connection to the Mastodon database."""

        return connect(host=host, database=database, user=user, password=password, port=port)

    engine = create_engine(f"postgresql+psycopg2://", creator=pg_connect)
    factory = sessionmaker(bind=engine)
    session = factory()
    return session
