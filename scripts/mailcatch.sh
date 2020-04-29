#!/usr/bin/env bash

docker run --rm -d -p 10025:1025 -p 1080:1080 --name mailcatcher schickling/mailcatcher
