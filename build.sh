#!/usr/bin/env bash -e
# Requires pandoc
# brew install pandoc

tox
# Don't move on to doc and requirements.txt update unless tests pass
pandoc --from=markdown --to=rst --output=README.rst README.md
pipenv install --dev
pipenv run pur -r requirements.txt
