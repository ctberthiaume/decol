#!/usr/bin/env bash -e

tox
pipenv install --dev
pipenv run pur -r requirements.txt
python setup.py sdist
python setup.py bdist_wheel --universal
