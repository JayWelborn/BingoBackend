SHELL := /bin/bash

test:
	coverage run bingo/manage.py test bingo/ -v 2
	coverage combine
	coverage html
	coverage report --fail-under=95

run:
	python bingo/manage.py runserver