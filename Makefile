.PHONY: image-app clean-image clean-container mysql-it create-db ingest-to-db image-data image-app docker-app-local kill-app-local aws-iden

clean-image:
	docker image prune

clean-container:
	docker rm $$(docker ps --filter status=exited -q)

mysql-it:
	docker run -it --rm \
		mysql:5.7.33 \
		mysql \
		-h$$MYSQL_HOST \
		-u$$MYSQL_USER \
		-p$$MYSQL_PASSWORD

create-db:
	docker run -it \
		-e MYSQL_HOST \
		-e MYSQL_PORT \
		-e MYSQL_USER \
		-e MYSQL_PASSWORD \
		-e MYSQL_DATABASE \
		pokemon_data run_rds.py create_db

ingest-to-db:
	docker run -it \
		-e MYSQL_HOST \
		-e MYSQL_PORT \
		-e MYSQL_USER \
		-e MYSQL_PASSWORD \
		-e MYSQL_DATABASE \
		pokemon_data run_rds.py ingest-csv

image-data:
	docker build -f Dockerfile_data -t pokemon_data .

image-app:
	docker build -f app/Dockerfile_app -t pokemon .

docker-app-local:
	docker run -p 5000:5000 --name test pokemon

kill-app-local:
	docker kill test

aws-iden:
	aws sts get-caller-identity

data/sample/pokemon.csv: run_s3.py
	docker run --mount type=bind,source="$(shell pwd)",target=/app/ \
		-e AWS_ACCESS_KEY_ID \
		-e AWS_SECRET_ACCESS_KEY \
		pokemon_data run_s3.py --download --local_path=data/sample/pokemon.csv --s3_path=s3://2021-msia423-wenyang-pan/raw/pokemon.csv

s3-raw: data/sample/pokemon.csv
