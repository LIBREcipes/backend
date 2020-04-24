#!/usr/bin/env bash

DIR=$(dirname $(readlink -f $0))/..

docker build -t librecipes-backend:latest $DIR

