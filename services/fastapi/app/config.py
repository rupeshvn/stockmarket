import os

class Settings:
    AIRFLOW_URL = os.getenv("AIRFLOW_URL")
    USERNAME = os.getenv("AIRFLOW_USER")
    PASSWORD = os.getenv("AIRFLOW_PASS")

settings = Settings()