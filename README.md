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
3. Run deploy_all.sh file
    - Creates a namespace for k3s
    - Helm is an app store. Helm stores the repo URL's locally so that it knows where to fetch the charts
    - With the install postgres command, helm first downloads the chart and then merges with values.yaml. It then generates the kubernetes yaml and sends to kubernetes api. It internally creates pod, service, pvc (storage) and secrets (passwords)
    - With the install airflow command, it internally creates a scheduler pod, webserver (API Server), Triggerer, DAG Processor, ConfigMaps and Secrets. The values.yaml ensures that it connects to Postgres not creating its own db
    
5. Deploy FastAPI
6. Trigger DAG via API

Some important commands:
1. If networking breaks, we can restart k3s with the below command:
    - sudo systemctl restart k3s

2. To check the nodes in k3s
    - kubectl get nodes

3. To get the pods in k3s
    - kubectl get pods
    - kubectl get pods -o wide

4. To describe the pods in k3s
    - kubectl describe pod <podname>

Some important learning targets:

1. Go inside a container and see the DAG files live
2. Trigger DAG and trace execution
3. Build API to trigger DAG


Issues Encountered:
1. Wifi was not connecting with PI. 
    Solution - Configured the country as India in one of the config files

2. If you dont have the ip of the PI, we can install nmap and find all ips connected to the wifi.
    Solution - The command used was 
        nmap -sn 192.168.29.0/24

3. Command used to connect with the wifi
    Solution - 
        sudo nmcli dev wifi connect "wifiname" password "actual_password"

4. DNS issue which is critical for Helm/Docker. Was getting "lookup auth.docker.io: i/o timeout"
    Solution - The solution was router DNS was unreliable. Configured DNS via Network Manager. The commands used are:
        sudo nmcli con mod "wifiname" ipv4.dns "8.8.8.8 1.1.1.1"
        sudo nmcli con mod "wifiname" ipv4.ignore-auto-dns yes
        sudo nmcli con down "wifiname"
        sudo nmcli con up "wifiname"

        When we run con down, the connection breaks. So we need to keep the ethernet cable handy 

5. Kubernetes network failure - I was getting "10.43.0.1:443 → no route to host". 
    Solution - Internal cluster networking was broken. Used the command
        sudo systemctl restart k3s

6. Kubernetes kept on crashing and restarting
    Solution - There was no swap memory configured. So when the memory usage spiked, k3s would crash and restart. Commands used are:
        sudo vim /etc/dphys-swapfile
        #set CONF_SWAPSIZE=2048
        sudo dphys-swapfile setup
        sudo dphys-swapfile swapon

7. Airflow UI was no accessible when i was using the url "http://192.168.29.178:8080"
    Solution - The airflow service was Cluster IP. It was not exposed externally. We need to first forward it the pi's port. Then we need to forward the local computer's port to pi's port.
    Command to run on pi:
        kubectl port-forward svc/airflow-api-server 8080:8080

    Commnad to run on personal laptop:
        ssh -L 8080:localhost:8080 pi@192.168.29.178

    After running the above commands on separate tabs, run the below:
        http://localhost:8080
