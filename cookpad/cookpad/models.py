from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from cookpad import settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE))


def create_recipes_raw_table(engine):
    """ Create recipes_raw table in DB.
    """
    DeclarativeBase.metadata.create_all(engine)


class RecipesRaw(DeclarativeBase):
    """Sqlalchemy recipes_raw model"""
    __tablename__ = "recipes_raw"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column('name', String)
    author = Column('author', String)
    description = Column('description', String)
    ingredients = Column('ingredients', JSON)
    instructions = Column('instructions', ARRAY(String))
    servings = Column('servings', String)
    link = Column('link', String)
    duration = Column('duration', String)
    category = Column('category', String)
