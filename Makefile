install:
	pip install -r requirements.txt

install-app:
	pip install -r app/requirements.txt

tests:
	cd app; pytest

start:
	cd app; uvicorn main:app --host=0.0.0.0 --port=5555 --reload

_heroku-deploy:
	git subtree push --prefix app heroku master

heroku-deploy: tests _heroku-deploy
	

