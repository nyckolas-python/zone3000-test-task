#!/bin/bash

set -e

MAX_WAIT_TIMEOUT=${MAX_WAIT_TIMEOUT:-60}

function wait_for() {
    if [ "$(which nc)" == "" ]; then
        echo
        echo "$(date '+%d.%m.%Y %H:%M:%S') Netcat can not be found. Install it before use this function."
        exit 1
    fi
    HOSTNAME=$1
    PORT=$2
    MAX_WAIT_TIMEOUT=$3
    IS_READY=false
    SLEEP_TIMEOUT=1
    I=0
    set +e
    while [ $IS_READY == false ]; do
        nc -z -w 1 ${HOSTNAME} ${PORT}
        [ $? == 0 ] && IS_READY=true
        printf "."
        sleep ${SLEEP_TIMEOUT}
        let I=${I}+${SLEEP_TIMEOUT}
        if [ ${I} -eq ${MAX_WAIT_TIMEOUT} ]; then
            echo
            echo "$(date '+%d.%m.%Y %H:%M:%S') Max wait timeout of waiting was exceeded."
            exit 1
        fi
    done
    echo
}

echo "Waiting till postgres database engine be available."
wait_for ${DB_HOST:-my_project_db} ${DB_PORT:-5432} ${MAX_WAIT_TIMEOUT}

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the Django server
python manage.py runserver 0.0.0.0:${BIND_PORT:-8000}