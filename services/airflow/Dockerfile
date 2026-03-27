FROM apache/airflow:3.1.7

# Switch to airflow user BEFORE installing packages
USER airflow

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt