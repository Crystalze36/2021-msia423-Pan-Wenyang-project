# MSiA423 Pokemon Recommender

Author: Wenyang Pan

QA: Xaiver Dong

## Project Charter 

#### Background 

[Pokemon](https://en.wikipedia.org/wiki/Pok%C3%A9mon#Gameplay_of_Pok%C3%A9mon) is a Japanese multimedia franchise, including video games, books, anime film series, live-action films, etc. The popularity of the Pokemon franchise starts from video games and one of the famous releases is the augmented reality mobile game Pokémon GO in 2016. The game players are the "Pokemon Trainers" and they try to capture Pokemons and train them.

#### Vision

When playing Pokemon video games, players can be overwhelmed by the vast information. The game includes more than 800 different Pokemons and each Pokemon has more than 20 attributes. Sometimes, the player might like a certain Pokemon and want to find Pokemon with similar characteristics for implementing a playing strategy. However, given the large number of Pokemons, it is hard to go over all of them and identify similar Pokemons manually. 

This app aims to solve this problem by building models based on existing Pokemon data and automatically finding the most similar Pokemons of a certain Pokemon. As a result, players can spend their time enjoying the game instead of reading through a Pokemon encyclopedia.

#### Mission

The user will input a name of Pokemon and the recommender will output 10 most similar Pokemons according to an underlying cluster algorithm. The data for this project comes from this [Pokemon dataset](https://www.kaggle.com/rounakbanik/pokemon). 

An example of running the app will look like the following. In a text input field, the user will input a Pokemon they like and the app will output some recommended Pokemons. For example, if the user input "Bulbasaur" (the name of a Pokemon), the app might output the following table, where each row represents a recommended Pokemon. 


|      | name       | type1 | link                                     |
| ---: | :--------- | :---- | :--------------------------------------- |
|    1 | Charmeleon | fire  | https://pokemondb.net/pokedex/Charmeleon |
|    2 | Wartortle  | water | https://pokemondb.net/pokedex/Wartortle  |

The actual format and recommended content in the app will probably be different than the table above. Specifically, the app will probably recommend more than 2 Pokemons and include some other features of each Pokemon, like location/environment found, counter type, etc. But the idea of recommending relevant Pokemons given user's input should remain the same.

#### Success Criteria

##### Machine Learning Metrics

Because the app uses an unsupervised clustering algorithm, we will not use fixed number of certain metrics as the deployment threshold. Instead, we will deploy the algorithm after identifying the best number of clusters with inertia and silhouette score and verifying the clustering algorithm is stable; that is, the model will predict similar clusters when we fit the model with half of the data and predict the cluster for the other half of the data.

Once the app goes live, we can calculate and monitor some other metrics, like the precision of recommendation by observing user behavior. For example, we can count a recommendation as correct when the user clicks the link to learn more about a recommended Pokemon. We can also conduct A/B testing to see whether a certain recommendation algorithm leads to higher precision.

##### Business Metrics

To determine the success of the app from a business perspective, we can measure the number of visits to the app and the user engagement to the Pokemon game. For user engagement, we might send surveys to the app users to learn more about their game performance and satisfaction after using the app. Overall, a successful deployment of the app will help Pokemon players to better explore and enjoy the game.



## Directory structure 

```
├── README.md                         <- You are here
├── api
│   ├── static/                       <- CSS, JS files that remain static
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── boot.sh                       <- Start up script for launching app in Docker container.
│   ├── Dockerfile                    <- Dockerfile for building image to run app  
│
├── config                            <- Directory for configuration files 
│   ├── local/                        <- Directory for keeping environment variables and other local configurations that *do not sync** to Github 
│   ├── logging/                      <- Configuration of python loggers
│   ├── flaskconfig.py                <- Configurations for Flask API 
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── external/                     <- External data sources, usually reference data,  will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── deliverables/                     <- Any white papers, presentations, final work products that are presented or delivered to a stakeholder 
│
├── docs/                             <- Sphinx documentation based on Python docstrings. Optional for this project. 
│
├── figures/                          <- Generated graphics and figures to be used in reporting, documentation, etc
│
├── models/                           <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks/
│   ├── archive/                      <- Develop notebooks no longer being used.
│   ├── deliver/                      <- Notebooks shared with others / in final state
│   ├── develop/                      <- Current notebooks being used in development.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports, helper functions, and SQLAlchemy setup. 
│
├── reference/                        <- Any reference material relevant to the project
│
├── src/                              <- Source data for the project 
│
├── test/                             <- Files necessary for running model tests (see documentation below) 
│
├── app.py                            <- Flask wrapper for running the model 
├── run.py                            <- Simplifies the execution of one or more of the src scripts  
├── requirements.txt                  <- Python package dependencies 
```

## Data Acquisition

The dataset used for this app comes from Kaggle. To download the data, you can go to this [website](https://www.kaggle.com/rounakbanik/pokemon) and click the Download button at the top of the page.    Note that you will need to register a Kaggle account in order to download dataset if you do not have one. 

### Interact with the data from S3

#### Build Docker Image

```
docker build -f Dockerfile_data -t pokemon_data .
```

#### Download Data from S3

```
docker run pokemon_data src/s3.py --download --local_path={your_local_path} --env AWS_ACCESS_KEY_ID --env AWS_SECRET_ACCESS_KEY
```

#### Upload Data to S3

```
docker run pokemon_data src/s3.py --s3_path={your_s3_path}
```

## Running the app

### 1. Initialize the database 

#### Create the database 
To create the database in the location configured in `config.py` run: 

`python run.py create_db --engine_string=<engine_string>`

By default, `python run.py create_db` creates a database at `sqlite:///data/pokemons.db`.

#### Adding pokemons 
To add pokemons to the database:

`python run.py ingest --engine_string=<engine_string> --name=<NAME> --type1=<TYPE1> --type2=<TYPE2>`

By default, `python run.py ingest` adds *Charizard* with type1 fire and type2 flying to the SQLite database located in `sqlite:///data/pokemons.db`.

#### Defining your engine string 
A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). 
##### Local SQLite database 

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/pokemons.db'
```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
engine_string = 'sqlite://////Users/martinpan/Repos/2021-msia423-wenyang-pan/data/pokemons.db'
```

### Remote MySQL Database

##### Export Connection Variables

````
source .mysqlconfig
echo $MYSQL_HOST
````

##### Connect to Database

```
docker run -it --rm \
    mysql:5.7.33 \
    mysql \
    -h$MYSQL_HOST \
    -u$MYSQL_USER \
    -p$MYSQL_PASSWORD
```

##### Build Docker Image

```
docker build -t pokemon_data .
```

##### Run Docker Container

```
docker run -it \
    --env MYSQL_HOST \
    --env MYSQL_PORT \
    --env MYSQL_USER \
    --env MYSQL_PASSWORD \
    --env DATABASE_NAME \
    pokemon_data run.py
```

