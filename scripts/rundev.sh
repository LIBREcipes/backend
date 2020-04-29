#!/usr/bin/env bash

DIR=$(dirname $(readlink -f $0))

export LR_EMAIL_HOST='127.0.0.1'
export LR_EMAIL_PORT=10025
export LR_EMAIL_HOST_USER=''
export LR_EMAIL_HOST_PASSWORD=''
export LR_EMAIL_USE_TLS='false'
export LR_DEFAULT_FROM_EMAIL='cooksel@madebit.be'

cd $DIR/..
pipenv run ./manage.py runserver 5000 --settings=librecipes.settings_dev
