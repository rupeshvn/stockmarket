import requests
import base64
from app.core.config import AIRFLOW_URL, USERNAME, PASSWORD


def trigger_dag_service(dag_id: str):
    url = f"{AIRFLOW_URL}/api/v2/dags/{dag_id}/dagRuns"

    credentials = f"{USERNAME}:{PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    response = requests.post(
        url,
        headers={
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json"
        },
        json={"conf": {}}
    )

    return {
        "status": response.status_code,
        "response": response.json()
    }