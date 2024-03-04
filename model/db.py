from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import declarative_base

from const import SQLALCHEMY_DATABASE_URL_MASTER

Base = declarative_base()


class dbSession:
    def __init__(self, db_url=SQLALCHEMY_DATABASE_URL_MASTER):
        self.engine = create_engine(db_url, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False)
        self.SessionThreadLocal = scoped_session(self.SessionLocal)

    @contextmanager
    def get_db(self):
        if self.SessionThreadLocal is None:
            raise Exception("Database not connected")
        session = self.SessionThreadLocal()
        try:
            yield session
        finally:
            session.close()

    def add(self, record):
        with self.get_db() as session:
            session.add(record)
            session.commit()
            session.refresh(record)
            return record.id

    def delete(self, record):
        record_id = record.id
        with self.get_db() as session:
            session.delete(record)
            session.commit()
            return record_id


class dbSessionread:
    def __init__(self, db_url=SQLALCHEMY_DATABASE_URL_MASTER):
        self.engine = create_engine(db_url, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, expire_on_commit=False)
        self.SessionThreadLocal = scoped_session(self.SessionLocal)

    @contextmanager
    def get_db_read(self):
        if self.SessionThreadLocal is None:
            raise Exception("Database not connected")
        session = self.SessionThreadLocal()
        try:
            yield session
        finally:
            session.close()