S3_PATH = s3://2021-msia423-wenyang-pan/raw/pokemon.csv
LOCAL_PATH = data/raw/pokemon.csv
FINAL_DATA_PATH = data/final/results.csv

# Docker Utility
.PHONY: image-data image-app clean-image clean-container

image-data:
	docker build -f Dockerfile_data -t pokemon_data_wpz3146 .

image-app:
	docker build -f app/Dockerfile_app -t pokemon_wpz3146 .

clean-image:
	docker image prune

clean-container:
	docker rm $$(docker ps --filter status=exited -q)

# File Utility
.PHONY: clean-data

clean-data:
	rm 'data/raw/pokemon.csv'
	rm 'data/interim/data_scale.csv'
	rm 'data/final/results.csv'
	rm 'data/msia423_pokemons.db'
	rm 'figures/cluster_selection.png'
	rm 'models/kmeans.joblib'

# AWS
.PHONY: aws-iden

aws-iden:
	aws sts get-caller-identity

# Database
.PHONY: mysql-it create-db ingest-to-db

mysql-it:
	docker run -it --rm \
		mysql:5.7.33 \
		mysql \
		-h$$MYSQL_HOST \
		-u$$MYSQL_USER \
		-p$$MYSQL_PASSWORD

create-db:
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ \
		-e SQLALCHEMY_DATABASE_URI \
		pokemon_data_wpz3146 run_rds.py create_db

ingest-to-db:
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ \
		-e SQLALCHEMY_DATABASE_URI \
		pokemon_data_wpz3146 run_rds.py ingest-csv --input_path=${FINAL_DATA_PATH}


# Model Pipeline
.PHONY: s3-upload, s3-raw, preprocess, train, recommend, model-all

s3-upload:
	docker run \
		-e AWS_ACCESS_KEY_ID \
		-e AWS_SECRET_ACCESS_KEY \
		pokemon_data_wpz3146 run_s3.py --local_path=${LOCAL_PATH} --s3_path=${S3_PATH}

data/raw/pokemon.csv: run_s3.py
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ \
		-e AWS_ACCESS_KEY_ID \
		-e AWS_SECRET_ACCESS_KEY \
		pokemon_data_wpz3146 run_s3.py --download --local_path=${LOCAL_PATH} --s3_path=${S3_PATH}

s3-raw: data/raw/pokemon.csv

data/interim/data_scale.csv: run_model.py config/model_config.yaml data/raw/pokemon.csv
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ \
		pokemon_data_wpz3146 run_model.py preprocess --input=data/raw/pokemon.csv --config=config/model_config.yaml

preprocess: data/interim/data_scale.csv

models/kmeans.joblib figures/cluster_selection.png: run_model.py config/model_config.yaml data/interim/data_scale.csv
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ \
		pokemon_data_wpz3146  run_model.py train --input=data/interim/data_scale.csv --config=config/model_config.yaml

train: models/kmeans.joblib figures/cluster_selection.png

data/final/results.csv: run_model.py config/model_config.yaml models/kmeans.joblib
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ \
		pokemon_data_wpz3146  run_model.py recommend --input=data/raw/pokemon.csv --config=config/model_config.yaml

recommend: data/final/results.csv

model-all: s3-raw preprocess train recommend

# App
.PHONY: docker-app-local kill-app-local

docker-app-local:
	docker run -e SQLALCHEMY_DATABASE_URI \
        --mount type=bind,source="$(shell pwd)",target=/app/ \
		-p 5000:5000 --name test pokemon_wpz3146

kill-app-local:
	docker kill test

# Test
.PHONY: test

test:
	docker run pokemon_data_wpz3146 -m pytest

# Theory of Everything
.PHONY: launch-in-one clean-all

launch-in-one: model-all create-db ingest-to-db docker-app-local

clean-all: clean-image clean-container clean-data