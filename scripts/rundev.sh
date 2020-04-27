#!/usr/bin/env bash

DIR=$(dirname $(readlink -f $0))

cd $DIR/..
pipenv run ./manage.py runserver 5000 --settings=librecipes.settings_dev
