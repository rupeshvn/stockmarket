#!/bin/bash

curl -sfL https://get.k3s.io | sh

echo "k3s installed"

sudo kubectl get nodes
