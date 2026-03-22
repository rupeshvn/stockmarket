#!/bin/bash

set -e  # stop on error

echo "Applying namespace..."
kubectl apply -f infra/namespaces.yaml

echo "Adding Helm repos..."
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add apache-airflow https://airflow.apache.org
helm repo update

echo "Installing Postgres..."
helm install postgres bitnami/postgresql -f infra/postgres/values.yaml

echo "Installing Airflow..."
helm install airflow apache-airflow/airflow -f infra/airflow/values.yaml

echo "Deployment triggered!"