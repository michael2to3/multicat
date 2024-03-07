from sqlalchemy import (
    create_engine,
    Table,
    Column,
    String,
    Boolean,
    MetaData,
    DateTime,
    select,
    func,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
import logging
from datetime import datetime, timedelta
from config import DATABASE_URL

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

Base = declarative_base()


class ConnectedClient(Base):
    __tablename__ = "connected_clients"
    client_id = Column(String, primary_key=True)
    last_heartbeat = Column(DateTime, server_default=func.now())
    busy = Column(Boolean, server_default="false")


class DatabaseOperations:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def register_client(self, client_id):
        with self.session_scope() as session:
            new_client = ConnectedClient(client_id=client_id)
            session.add(new_client)
        logger.info(f"Client {client_id} registered.")

    def unregister_client(self, client_id):
        with self.session_scope() as session:
            session.query(ConnectedClient).filter(
                ConnectedClient.client_id == client_id
            ).delete()
        logger.info(f"Client {client_id} unregistered.")

    def update_client_heartbeat(self, client_id):
        with self.session_scope() as session:
            client = (
                session.query(ConnectedClient)
                .filter(ConnectedClient.client_id == client_id)
                .first()
            )
            if client:
                client.last_heartbeat = datetime.now()
        logger.info(f"Updated heartbeat for client {client_id}.")

    def cleanup_inactive_clients(self):
        with self.session_scope() as session:
            inactive_threshold = datetime.now() - timedelta(minutes=5)
            session.query(ConnectedClient).filter(
                ConnectedClient.last_heartbeat < inactive_threshold
            ).delete()
        logger.info("Inactive clients cleaned up.")
