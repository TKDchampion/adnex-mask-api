from fastapi import FastAPI

app = FastAPI(
    title="Pharmacy API",
    description="A simple API to manage pharmacies",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Pharmacy API"}