.PHONY: image-app

docker-clean-im:
	docker image prune

docker-bye-container:
	docker rm $(docker ps --filter status=exited -q)

image-app:
	docker build -f app/Dockerfile_app -t pokemon .

docker-app-local:
	docker run -p 5000:5000 --name test pokemon

kill-app-local:
	docker kill test
