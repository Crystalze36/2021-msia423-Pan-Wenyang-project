# MSiA423 Pokemon Recommender

Author: Wenyang Pan

QA: Xaiver Dong

## Project Charter 

<img src="figures/pokemon_show.png" alt="drawing" height="300" width="360"/>



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
├── run_s3.py                         <- Download and Upload data from/to S3
├── run_rds.py                        <- Create and update table in RDS
├── requirements.txt                  <- Python package dependencies 
```



## Setup

### Software Requirements

+ If you want to run the code in this project repo locally, you need to have python 3.6 or above. 
+ In the Docker image ​whale:, we use Python 3.6.9 as the running python version.

### Environment Variable

#### AWS Credential

You need to have two environment variables - `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`  setup in your computer to run the following commands with S3. A simple way to do this run the following two lines in your terminal shell. Note that you need to replace "YOUR_ACCESS_KEY_ID" and "YOUR_SECRET_ACCESS_KEY" to your real id and secret access key. 

```bash
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_ACCESS_KEY"
```

#### RDS Credential

### Docker Image :whale:

This project relies on two Docker image to run the command.  You can build these two images with the following command.

```bash
make image-data
make image-app
```

+ The `make image-data` will produce a Docker image called `pokemon_data`, which are used to get the raw data, run the model pipeline, and interact with database. 
+ The `make image-app` will produce a Docker image called `pokemon`, which are used to launch the flask app. 

## Data Source

The dataset used for this app comes from Kaggle. To download the data, you can go to this [website](https://www.kaggle.com/rounakbanik/pokemon) and click the Download button at the top of the page.    Note that you will need to register a Kaggle account in order to download dataset if you do not have one. Because the dataset is relatively small, we also save a copy in `data/raw/pokemon.csv`. Another copy is also uploaded to s3 and we will describe how to download the data from s3. If you want to upload this data to your own S3 bucket,  see this optional section below.

#### [Optional] Upload data to S3


 To upload the data to S3 with docker, you can run the following command. You need to specify your local data path and s3 data path by replacing the `{your_local_path}` and `{your_s3_path}` below. The default `S3_PATH` is `'s3://2021-msia423-wenyang-pan/raw/pokemon.csv'`and the default `LOCAL_PATH` is `data/raw/pokemon.csv`.
```bash
make s3-upload LOCAL_PATH={your_local_path} S3_PATH={your_s3_path}
```
## Model Pipeline

### Whole Model Pipeline

You can run the whole model pipeline with the following the command.

```bash
make model-all
```

This command will run the whole model pipeline, including downloading the raw data from s3, preprocessing the data, training the model and generating the recommendation results. The final output is stored in `data/final/results.csv`. Next, we will describe how to run each step in the in the pipeline and the location of artifacts produced from each step. Note that those four steps below need to be run sequentially. 

### Download Raw Data from S3

You can download the data from s3 to local with the following command. You can specify your S3 path by replacing the `{your_s3_path}` below. The default `S3_PATH` is `'s3://2021-msia423-wenyang-pan/raw/pokemon.csv'`. This step will store the raw data to `data/raw/pokemon.csv`.

```bash
make s3-raw S3_PATH={your_s3_path}
```

### Preprocess Data

You can preprocess the data with `make preprocess`, which will store the preprocessed data to `data/interim/data_scale.csv`.

### Train Model

You can train the model with `make train`, which will store the trained model to `models/kmeans.joblib` and the cluster selection plot to `figures/cluster_selection.png`.

### Generate Recommendation Results

You can generate the recommendation results with `make recommend`, which will store the results in `data/final/results.csv`.

## Store Results in Database

### Database

#### Create the Database

To create the database in the location configured in `config.py` run: 

`python run_rds.py create_db --engine_string=<engine_string>`

By default, `python run.py create_db` creates a database at `sqlite:///data/pokemons.db`. Note that you can also change the `engine_string` by changing the content `<engine_string>` above or set an environment variable `SQLALCHEMY_DATABASE_URI`.

#### Adding pokemons 

To add pokemons to the database:

`python run_rds.py ingest --engine_string=<engine_string> --name=<NAME> --type1=<TYPE1> --type2=<TYPE2>`

By default, `python run_rds.py ingest` adds *Charizard* with type1 fire and type2 flying to the SQLite database located in `sqlite:///data/pokemons.db`.

#### Note on engine_string

A SQLAlchemy database connection is defined by a string with the following format:

`dialect+driver://username:password@host:port/database`

The `+dialect` is optional and if not provided, a default is used. For a more detailed description of what `dialect` and `driver` are and how a connection is made, you can see the documentation [here](https://docs.sqlalchemy.org/en/13/core/engines.html). 

#### Local Database configuration 

A local SQLite database can be created for development and local testing. It does not require a username or password and replaces the host and port with the path to the database file: 

```python
engine_string='sqlite:///data/pokemons.db'
```

The three `///` denote that it is a relative path to where the code is being run (which is from the root of this directory).

You can also define the absolute path with four `////`, for example:

```python
engine_string = 'sqlite://////Users/martinpan/Repos/2021-msia423-wenyang-pan/data/pokemons.db'
```

#### Remote Database Connection

##### Prerequisites

In order to proceed with the following command, you need to satisfy the following requirements:

1. You need to connect to the northwestern VPN

2. You should have the `pokemon_data` image built as described in the Docker Image section.

3. If you need to have connection variables set up in your environment variables. You should have 5 variables: `MYSQL_USER`, `MYSQL_PASSWORD`,  `MYSQL_HOST`,  `MYSQL_PORT `, `MYSQL_DATABASE`. Like we describe in the AWS credential section, you can setup your environment variables with the following. Note that you need to replace these with your actual connection credentials. 

   ```bash
   export MYSQL_USER="YOUR_SQL_USER_NAME"
   export MYSQL_PASSWORD="YOUR_SQL_PASSWORD"
   export MYSQL_HOST="YOUR_SQL_HOST"
   export MYSQL_PORT="YOUR_SQL_PORT"
   export MYSQL_DATABASE="YOUR_DATABASE_NAME"
   ```

##### Test Connection to Database

You can run the following to test whether you can connect to the database. 

```
docker run -it --rm \
    mysql:5.7.33 \
    mysql \
    -h$MYSQL_HOST \
    -u$MYSQL_USER \
    -p$MYSQL_PASSWORD
```

If succeed, you should be able to enter an interactive mysql session and you can show all databases you have with the command: `show databases;`.

##### Create Databases 

You can create a new databases with the following command. By default, the script uses the engine string specified in `config/flaskconfig.py`.

```
docker run -it \
    -e MYSQL_HOST \
    -e MYSQL_PORT \
    -e MYSQL_USER \
    -e MYSQL_PASSWORD \
    -e MYSQL_DATABASE \
    pokemon_data run_rds.py create_db --engine_string={your_engine_string}
```

##### Add information to the Databases

You can add information about a Pokemon with the following command. By default, the script uses the engine string specified in `config/flaskconfig.py`. The default added Pokemon is "Charizard", with "fire" as type1 and "flying" as type2. Note that the database created from the command above does not allow duplicate names. Thus, you might receive an error message if you try to insert a pokemon with same name twice.

```
docker run -it \
    -e MYSQL_HOST \
    -e MYSQL_PORT \
    -e MYSQL_USER \
    -e MYSQL_PASSWORD \
    -e MYSQL_DATABASE \
    pokemon_data run_rds.py ingest --engine_string={your_engine_string} --name={pokemon name} --type1={1st type} --type2={2nd type}
```

#### Examine the Database

##### Locally 

If you create the database locally, you can view your result by using any sqlite client, such as [DB Browser](https://sqlitebrowser.org/), to open the `.db` file created after running the `run_rds.py` file. 

##### Remote

You can reenter the mysql interactive session by using the command under section [Test Connection to Database](#test-connection-to-database). Then you can type the following command to examine whether the table was created. Note that you need to replace `<your_target_database_name>` to the real database name. 

```
show databases;
use <your_target_database_name>;
show tables; 
```



## Launch App



## Unit Test

