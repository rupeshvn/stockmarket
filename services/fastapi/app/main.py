from fastapi import FastAPI
import requests
import os
import base64

app = FastAPI()

AIRFLOW_URL = os.getenv("AIRFLOW_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/trigger/{dag_id}")
def trigger_dag(dag_id: str):
    url = f"{AIRFLOW_URL}/api/v2/dags/{dag_id}/dagRuns"
    credentials = f"{USERNAME}:{PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    response = requests.post(
        url,
        headers={
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"},
        json={"conf": {}}
    )

    return {
        "status": response.status_code,
        "response": response.json()
    }