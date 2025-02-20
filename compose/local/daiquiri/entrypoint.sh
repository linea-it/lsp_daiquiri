#!/bin/bash

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

# psycopg2.connect(
#     dbname="${DB_DATABASE}",
#     user="${DB_USER}",
#     password="${DB_PASSWORD}",
#     host="${DB_HOST}",
#     port="${DB_PORT}",
# )

postgres_ready() {
python << END
import sys

import psycopg2

try:
    psycopg2.connect("${DATABASE_APP}")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)

END
}
until postgres_ready; do
    >&2 echo 'Waiting for PostgreSQL to become available...'
    sleep 1
done
>&2 echo 'PostgreSQL is available'

exec "$@"
