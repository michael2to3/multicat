from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
Base = declarative_base()


class Database:
    def __init__(self, database_url):
        self.engine = create_engine(database_url, pool_pre_ping=True)
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=self.engine
            )
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database connection established")
        except OperationalError:
            logger.error("Database connection failed")

    @contextmanager
    def session(self):
        session = scoped_session(self.SessionLocal)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.remove()
