SHELL := /bin/bash

test:
	coverage run --branch bingo/manage.py test bingo/
	coverage report --fail-under=95
	coverage html

run:
	python bingo/manage.py runserver