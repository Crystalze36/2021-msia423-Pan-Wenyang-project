import logging

import pandas as pd
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)

Base = declarative_base()


class Pokemon(Base):
    """
    Create a data model for the database to be set up for capturing Pokemon info
    """

    __tablename__ = 'pokemons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    input = Column(String(100), unique=False, nullable=False)
    the_rank = Column(Integer, unique=False, nullable=False)
    recommendation = Column(String(100), unique=False, nullable=False)
    type1 = Column(String(100), unique=False, nullable=False)
    type2 = Column(String(100), unique=False, nullable=True)
    abilities = Column(String(100), unique=False, nullable=True)
    generation = Column(Integer, unique=False, nullable=False)
    learn_more = Column(Text, unique=False, nullable=False)

    __table_args__ = (UniqueConstraint('input', 'recommendation', name='unique_pair'),
                      )

    def __repr__(self):
        return f'Pokemon name: {self.input}, type1: {self.type1}, type2: {self.type2}'


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

    def add_pokemon_rec(self, name: str, the_rank: int, rec: str,
                        type1: str, type2: str, abilities: str,
                        generation: int, learn_more: str) -> None:
        """Seeds an existing database with additional Pokemons.
        Args:
            name (str): name of the pokemon
            the_rank (int):
            rec (str):
            type1 (str): the first type of that pokemon
            type2 (str): the second type of that pokemon
            abilities (str):
            generation (int):
            learn_more (str):
        Returns:None
        """

        session = self.session
        pokemon = Pokemon(input=name, the_rank=the_rank, recommendation=rec,
                          type1=type1, type2=type2, abilities=abilities,
                          generation=generation, learn_more=learn_more)
        session.add(pokemon)
        session.commit()
        logger.info(f"Pokemon {name} with {rec} was added to the database")

    def add_pokemon_rec_df(self, input_path: str) -> None:

        session = self.session
        persist_list = []
        data_list = pd.read_csv(input_path).to_dict(orient='records')

        for data in data_list:
            persist_list.append(Pokemon(**data))
        session.add_all(persist_list)

        session.commit()
        logger.info(f'{len(persist_list)} records were added to the table')
