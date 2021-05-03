import argparse

import logging.config

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('pokemon-pipeline')

from src.manage_pokemon import PokemonManager, create_db
from config.flaskconfig import SQLALCHEMY_DATABASE_URI

if __name__ == '__main__':

    # Add parsers for both creating a database and adding songs to it
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
    subparsers = parser.add_subparsers(dest='subparser_name')

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database")
    sb_create.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    sb_ingest.add_argument("--name", default="Charizard", help="Name of Pokemon to be added")
    sb_ingest.add_argument("--type1", default="fire", help="Type 1 of the added Pokemon")
    sb_ingest.add_argument("--type2", default="flying", help="Type 2 of the added Pokemon")
    sb_ingest.add_argument("--engine_string", default='sqlite:///data/pokemons.db',
                           help="SQLAlchemy connection URI for database")

    args = parser.parse_args()
    sp_used = args.subparser_name
    if sp_used == 'create_db':
        create_db(args.engine_string)
    elif sp_used == 'ingest':
        tm = PokemonManager(engine_string=args.engine_string)
        tm.add_pokemon(args.name, args.type1, args.type2)
        tm.close()
    else:
        parser.print_help()
