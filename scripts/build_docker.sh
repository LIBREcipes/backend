#!/usr/bin/env bash

DIR=$(dirname $(readlink -f $0))/..
TAG=latest
BUILD=true
PUSH=false
DEPLOY=false
DEPLOY_HOST=''


# Use GNU getopt to parse command line arguments
if ! ARGUMENTS=$(getopt -o t:nd:p --long tag:,deploy:,no-build,push -- "$@"); then
  echo "Failed to parse command-line arguments"
  exit 1
fi
eval set -- "$ARGUMENTS"

while true; do
  case "$1" in
    -t | --tag)
      TAG=$2
      shift
    ;;

    -d|--deploy)
      DEPLOY=true
      DEPLOY_HOST="$2"
      shift
    ;;

    -n|--no-build)
      BUILD=false
    ;;

    -p|--push)
      PUSH=true
      ;;

    --)
      break
      ;;
    
    *)
      echo 'error'
      exit 1
      ;;
  esac
  shift
done

$BUILD && {
  echo 'Building...'
  docker build -t mattydebie/librecipes-backend:$TAG $DIR
}

$PUSH && {
  echo 'Pushing to dockerhub...'
  docker push mattydebie/librecipes-backend:$TAG
}

$DEPLOY && {
  $PUSH && sleep 5
  echo "Deploying to ${DEPLOY_HOST}"
  ssh $DEPLOY_HOST <<EOF
mkdir cooksel -p
cd cooksel
docker-compose pull api
docker-compose up -d
docker-compose exec api ./manage.py migrate
docker-compose exec api ./manage.py collectstatic
EOF
}


