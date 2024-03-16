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
    _instance = None

    def __new__(cls, database_url=None):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            try:
                cls._instance.engine = create_engine(database_url, pool_pre_ping=True)
                with cls._instance.engine.connect() as connection:
                    connection.execute(text("SELECT 1"))
                cls._instance.SessionLocal = sessionmaker(
                    autocommit=False, autoflush=False, bind=cls._instance.engine
                )
                Base.metadata.create_all(bind=cls._instance.engine)
                logger.info("Database connection established")
            except OperationalError:
                logger.error("Database connection failed")
        return cls._instance

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
