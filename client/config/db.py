import logging
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

logger = logging.getLogger(__name__)
Base = declarative_base()


class Database:
    _instance = None

    def __new__(cls, database_url=None):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.database_url = database_url
            cls._initialize_engine()
        return cls._instance

    @classmethod
    def _initialize_engine(cls):
        try:
            cls._instance.engine = create_engine(
                cls._instance.database_url, pool_pre_ping=True
            )
            with cls._instance.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            cls._instance.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=cls._instance.engine
            )
            Base.metadata.create_all(bind=cls._instance.engine)
            logger.info("Database connection established")
        except OperationalError:
            logger.error("Database connection failed, unable to establish")
            raise

    @contextmanager
    def session(self):
        if not hasattr(self, "SessionLocal"):
            logger.info(
                "SessionLocal is missing, attempting to reconnect to the database"
            )
            self._initialize_engine()

        session = scoped_session(self.SessionLocal)
        try:
            yield session
            session.commit()
        except OperationalError as e:
            logger.error(
                "OperationalError encountered, attempting to reset database connection"
            )
            session.rollback()
            session.remove()
            self._initialize_engine()
            raise OperationalError(
                "Database reconnection attempted after OperationalError: " + str(e)
            )
        except Exception:
            session.rollback()
            raise
        finally:
            session.remove()
