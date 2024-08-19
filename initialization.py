import logging

from models.database import engine
from models.task import Base

logger = logging.getLogger(__name__)


def create_tables():
    """
    Create all tables in the database using the models defined with Base.
    This function is called at the startup of the application.
    """
    logger.info("Creating tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tables created.")
