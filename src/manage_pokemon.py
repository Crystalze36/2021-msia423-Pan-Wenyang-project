import logging.config

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()


class Pokemon(Base):
    """
    Create a data model for the database to be set up for capturing Pokemon info
    """

    __tablename__ = 'pokemons'

    id = Column(Integer, primary_key=True)
    english_name = Column(String(100), unique=True, nullable=False)
    type1 = Column(String(100), unique=False, nullable=False)
    type2 = Column(String(100), unique=False, nullable=True)

    def __repr__(self):
        return f'Pokemon name: {self.english_name}'


def create_db(engine_string: str) -> None:
    """Create database from provided engine string
    Args:
        engine_string (str): Engine string
    Returns: None
    """
    engine = sqlalchemy.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logger.info("Database created.")


class PokemonManager:

    def __init__(self, app=None, engine_string=None):
        """
        Args:
            app (Flask): Flask app
            engine_string (str): Engine string
        """
        if app:
            self.db = SQLAlchemy(app)
            self.session = self.db.session
        elif engine_string:
            engine = sqlalchemy.create_engine(engine_string)
            Session = sessionmaker(bind=engine)
            self.session = Session()
        else:
            raise ValueError("Need either an engine string or a Flask app to initialize")

    def close(self) -> None:
        """Closes session
        Returns: None
        """
        self.session.close()

    def add_pokemon(self, name: str, type1: str, type2: str) -> None:
        """Seeds an existing database with additional Pokemons.
        Args:
            name (str): name of the pokemon
            type1 (str): the first type of that pokemon
            type2 (str): the second type of that pokemon
        Returns:None
        """

        session = self.session
        pokemon = Pokemon(english_name=name, type1=type1, type2=type2)
        session.add(pokemon)
        session.commit()
        logger.info(f"Pokemon {name} with type {type1} and {type2} was added to the database")
