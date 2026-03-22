# Pi Data Platform

Architecture:
FastAPI → Airflow → Kubernetes → Postgres

## Setup Steps
1. Clone repo
    git clone git@github.com-stockmarket:rupeshvn/stockmarket.git
    cd stockmarket
2. Setup k3s
    bash infra/k3s/setup.sh
    sudo vim /boot/firmware/cmdline.txt (Add the text - cgroup_memory=1 cgroup_enable=memory)
    sudo apt install iptables -y
    sudo chown pi:pi /etc/rancher/k3s/k3s.yaml
    export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
    echo 'export KUBECONFIG=/etc/rancher/k3s/k3s.yaml' >> ~/.bashrc
    source ~/.bashrc
2. Install Helm
3. Deploy Postgres
4. Deploy Airflow
5. Deploy FastAPI
6. Trigger DAG via API