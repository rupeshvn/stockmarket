from fastapi import APIRouter
import requests
from .config import settings

router = APIRouter()

@router.post("/run-job/{dag_id}")
def run_job(dag_id: str):
    response = requests.post(
        f"{settings.AIRFLOW_URL}/dags/{dag_id}/dagRuns",
        auth=(settings.USERNAME, settings.PASSWORD),
        json={}
    )
    return response.json()