# Adnex Mask API

This is a mask API application that interacts with a database. You can either set up the environment manually or directly start a Docker container. Once set up, you can start using it.

[Demo api](https://)

## Envirement

### Version

- python v3.9
- Docker v20.10.14
- postgresql @15

### Env file

```javascript
// POSTGRES
POSTGRES_USER=postgres
POSTGRES_PASSWORD=XXX
POSTGRES_DB=XXX_database
DB_HOST=db
DB_PORT=5432

// Database connection
DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DB_HOST}:${DB_PORT}/${POSTGRES_DB}
```

## Docker (Recommend)

```javascript
docker-compose up
```

## Build & Run

### 1. Virtual (Optional)

```javascript
python -m venv venv
```

- Window
  ```javascript
  venv\Scripts\activate
  ```
- Mac
  ```javascript
  source venv/bin/activate
  ```

### 2. Install libraries

```javascript
pip install -r requirements.txt
```

### 3. Migration DB & Import Data

```javascript
// Alembic migration
alembic upgrade head

// import data
python -m etl.import_pharmacies data/pharmacies.json
python -m etl.import_users data/users.json
```

### 4. Run server

```javascript
uvicorn app.main:app --reload
```

## Test

### Doc & UI

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Unit test

- test_opening_hours.py
  ```javascript
  pytest tests/test_opening_hours.py
  ```
- all
  ```javascript
  pytest;
  ```
