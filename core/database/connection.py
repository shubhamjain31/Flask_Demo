from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from flask_sqlalchemy import SQLAlchemy

from config import settings

POSTGRES_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOSTNAME}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(
    POSTGRES_URL, echo=True
)

db = SQLAlchemy()

SessionLocal    = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session         = SessionLocal()

class Base_Model:

    @classmethod
    def model_lookup_by_table_name(cls, table_name):
        metadata_obj = MetaData()
        metadata_obj.reflect(bind=engine)

        for table in metadata_obj.tables.values():
            if table.name == table_name:
                return table
            
    @classmethod
    def list_of_tables(cls):
        metadata_obj = MetaData()
        metadata_obj.reflect(bind=engine)

        return metadata_obj.tables.keys()
    
Base = declarative_base(cls=Base_Model)