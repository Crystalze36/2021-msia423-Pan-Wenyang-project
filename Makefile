.PHONY: flask-debug

flask-debug:
	export FLASK_DEBUG=1
	flask run