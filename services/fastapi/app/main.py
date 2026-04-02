from fastapi import FastAPI
from api.stocks import router as stock_router
from api.airflow import router as airflow_router

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

app.include_router(stock_router)
app.include_router(airflow_router)