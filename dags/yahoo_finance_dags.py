from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import yfinance as yf
import psycopg2

def fetch_and_store():
    data = yf.download("AAPL", period="1d")

    conn = psycopg2.connect(
        host="postgres-postgresql",
        database="airflowdb",
        user="airflow",
        password="airflowpass"
    )

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock_data (
            date TIMESTAMP,
            open FLOAT,
            close FLOAT
        )
    """)

    for index, row in data.iterrows():
        cur.execute(
            "INSERT INTO stock_data (date, open, close) VALUES (%s, %s, %s)",
            (index, row['Open'], row['Close'])
        )

    conn.commit()
    cur.close()
    conn.close()

with DAG(
    "yahoo_stock",
    start_date=datetime(2024,1,1),
    schedule_interval=None,
    catchup=False
) as dag:

    task = PythonOperator(
        task_id="fetch_stock",
        python_callable=fetch_and_store
    )