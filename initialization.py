from models.database import engine
from models.task import Base


def create_tables():
    """
    Create all tables in the database using the models defined with Base.
    This function should be called at the startup of the application.
    """
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created.")
