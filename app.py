import traceback
import logging.config

from flask import Flask
from flask import render_template, request

from src.manage_pokemon import PokemonManager, Pokemon

# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Web app log')

# Initialize the database session
pokemon_manager = PokemonManager(app)


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/', methods=['POST'])
def data():
    if request.method == 'POST':
        user_input = request.form.to_dict()['pokemon_name']
        user_input = str(user_input).lower()
        try:
            pokemons = pokemon_manager.session.query(Pokemon).filter_by(input=user_input).limit(
                app.config["MAX_ROWS_SHOW"]).all()
            if len(pokemons) == 0:
                return render_template('not_found.html', user_input=user_input)
            return render_template('index.html', pokemons=pokemons, user_input=user_input)
        except:
            traceback.print_exc()
            logger.warning("Not able to display tracks, error page returned")
            return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
