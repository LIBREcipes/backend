#!/usr/bin/env bash

DIR=$(dirname $(readlink -f $0))

cd $DIR/..

pipenv run ./manage.py $@ --settings=librecipes.settings_dev
