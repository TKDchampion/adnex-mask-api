from fastapi import FastAPI
import psycopg2
from app.database import DATABASE_URL
from app.routers import ROUTERS

app = FastAPI(
    title="Pharmacy API",
    description="A simple API to manage pharmacies",
    version="1.0.0"
)

for router in ROUTERS:
    app.include_router(router.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Pharmacy API"}

@app.get("/db-test")
def test_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        conn.close()
        return {"db_version": db_version}
    except Exception as e:
        return {"error": str(e)}