#!/bin/sh
DB_HOST=$(echo $DATABASE_URL | sed -E 's/.*@([^:/]+).*/\1/')
DB_PORT=$(echo $DATABASE_URL | sed -E 's/.*:([0-9]+)\/.*/\1/')

echo "Waiting for PostgreSQL to start at $DB_HOST:$DB_PORT..."

MAX_RETRIES=60
COUNTER=0

while ! python -c "
import psycopg2, time, sys
from urllib.parse import urlparse
try:
    url = urlparse('$DATABASE_URL')
    conn = psycopg2.connect(
        dbname=url.path[1:], 
        user=url.username, 
        password=url.password, 
        host=url.hostname, 
        port=url.port
    )
    conn.close()
    sys.exit(0)
except Exception as e:
    print('Retry', $COUNTER, 'Waiting for PostgreSQL...', str(e))
    time.sleep(1)
    sys.exit(1)
"; do
  COUNTER=$((COUNTER + 1))
  if [ $COUNTER -ge $MAX_RETRIES ]; then
    echo "Error: PostgreSQL did not start within the timeout period."
    exit 1
  fi
done
echo "PostgreSQL started"

# Alembic migration
alembic upgrade head

# import data
python -m etl.import_pharmacies data/pharmacies.json
python -m etl.import_users data/users.json

PORT=${PORT:-8000}

# start FastAPI
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
