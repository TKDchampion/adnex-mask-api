#!/bin/sh

echo "Waiting for PostgreSQL to start..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL started"

# Alembic migration
alembic upgrade head

# import data
python -m etl.import_pharmacies data/pharmacies.json
python -m etl.import_users data/users.json

# start FastAPI
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
