from fastapi import FastAPI
import requests
import os

app = FastAPI()

AIRFLOW_URL = os.getenv("AIRFLOW_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/trigger/{dag_id}")
def trigger_dag(dag_id: str):
    url = f"{AIRFLOW_URL}/api/v1/dags/{dag_id}/dagRuns"

    response = requests.post(
        url,
        auth=(USERNAME, PASSWORD),
        json={}
    )

    return {
        "status": response.status_code,
        "response": response.json()
    }