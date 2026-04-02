from fastapi import APIRouter
from services.airflow_service import trigger_dag_service

router = APIRouter()

@router.post("/trigger/{dag_id}")
def trigger_dag(dag_id: str):
    return trigger_dag_service(dag_id)