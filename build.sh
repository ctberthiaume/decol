#!/usr/bin/env bash -e

pipenv install --dev
pipenv run pur -r requirements.txt
tox
python setup.py sdist
python setup.py bdist_wheel --universal
