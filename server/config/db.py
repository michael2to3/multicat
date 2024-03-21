import logging
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
Base = declarative_base()


class Database:
    _instance = None

    def __new__(cls, database_url=None):
        if cls._instance is None:
            if database_url is None:
                logger.error("Database URL is not provided")
                raise ValueError("Database URL must be provided")

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
            except OperationalError as e:
                logger.error(f"Database connection failed: {str(e)}")
                raise

        return cls._instance

    @contextmanager
    def session(self):
        if not hasattr(self, "SessionLocal"):
            logger.error(
                "'SessionLocal' is not initialized. Ensure 'Database' is properly instantiated with a database URL."
            )
            raise AttributeError(
                "'SessionLocal' is not initialized. Ensure 'Database' is properly instantiated with a database URL."
            )

        session = scoped_session(self.SessionLocal)
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Session rollback due to exception: {e}")
            raise
        finally:
            session.remove()
