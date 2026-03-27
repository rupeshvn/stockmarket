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
    
4. Store normal variables on Git and secrets in kubernetes cluster
    - Create a .env file on pi in the same git folder (it is never tracked)
    - Store the secrets in that env file
    - Run the command
        kubectl create secret generic fastapi-secret \
            --from-env-file=.env\
            --dry-run=client -o yaml | kubectl apply -f -
        This command generates the yaml file and then applies it to the cluster

5. Update the Fastapi code and create docker image and push
    - Signed up on docker using codewithrupeshv gmail
    - Username as rupeshvn
    - Run the following commands on our laptop
        - sudo apt update
        - sudo apt install docker.io -y
        - sudo usermod -aG docker $USER
        - docker --version (to verify)
        - docker login (stores creds to our local automatically)
    - We need to have multi arch builds because the image we build from our laptop would be of our laptop architecture. It might not run on pi architecture. Run the below commands on our laptop
        - sudo apt update
        - sudo apt install ca-certificates curl gnupg -y
        - sudo apt install -m 0755 -d /etc/apt/keyrings
        - curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        - echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu jammy stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        - sudo apt update
        - sudo apt install docker-buildx-plugin -y
        - docker buildx version (verify buildx version)
    - Buildx will not work with default docker driver. We need docker-container driver. Below are the commands
        - docker buildx create --name mybuilder --driver docker-container
        - docker buildx use mybuilder
        - docker buildx inspect --bootstrap
            (this downloads the required buildkit containers and enables multi arch support)
        - docker buildx ls
            (we can check the driver being used by buildx)
    - Create a build_and_push.sh file in scripts
        - chmod +x scripts/build_and_push.sh (gives it execute permission)
        - /scripts/build_and_push.sh

    - Deploy the fastapi code
        - Take the latest pull on pi and run the below commands
            - kubectl apply -f infra/fastapi/deployment.yaml
            - kubectl apply -f infra/fastapi/service.yaml
        
        - To get the services ip and ports on pi, we can run 
            - kubectl get svc

Pending things:
    - Issue was that the airflow scheduler was not having yfinance which is why the dag was not getting imported. Now creating it via docker image and deploying it

    - run the command till its successful 
        -curl -X POST http://192.168.29.178:30007/trigger/yahoo_finance_dag        
    

    
        - 
Deploy FastAPI
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

5. Normally kubernetes restarts automatically on every boot. To check if its enabled we can run the below command:
    - sudo systemctl is-enabled k3s

6. To get the cluster ip and nodes
    - kubectl get svc

7. Whenever we push a new fastapi image to docker, to get it deployed we need to run the command
    - kubectl rollout restart deployment fastapi

8. If you make any changes in the values.yaml file of airflow in infra, then we need to run the below command
    - helm upgrade airflow apache-airflow/airflow -f infra/airflow/values.yaml

9. If any changes are not getting applied, we can delete the pods and it will get recreated
    - kubectl delete pod \
airflow-api-server-7cf7fdb96b-j6tpb \
airflow-dag-processor-fd6c897cc-l4kj5 \
airflow-scheduler-0 \
airflow-triggerer-0

Some important learning targets:

1. Go inside a container and see the DAG files live
2. Trigger DAG and trace execution
3. Build API to trigger DAG


Some important pi and laptop commands:
1. If you want to check all the ips connected to the wifi on laptop
    nmap -sn 192.168.29.0/24

2. To get the wifi ip on pi
    ip addr show wlan0

3. To get the wifi details on your pi run on pi
    nmcli dev wifi list
    If i cannot see my 5ghz wifi connection in it then its because the wifi connection channel would not be in the range of 36-48. We can see the channel of our wifi, we can run the below command on our laptop:
        iw dev
    Switching off and on our wifi can change the channel

4. To see all the connections on our pi
    nmcli connections show

5. To check the priority of our connections on pi
    nmcli connection show "<wifi name>" | grep autoconnect-priority

6. To modify the auto connection priority
    sudo nmcli connection modify "rupsnowy" connection.autoconnect-priority 20
    sudo nmcli connection modify "rupsnowy" connection.autoconnect yes

    similarly update the auto connect priority of other wifi as well

7. To restart the network manager on pi
    sudo systemctl restart NetworkManager

8. To check which wifi our pi is connected to 
    nmcli device status

9. To see the hidden folders
    ls -a



Issues Encountered:
1. Wifi was not connecting with PI. 
    Solution - Configured the country as India in one of the config files

2. If you dont have the ip of the PI, we can install nmap and find all ips connected to the wifi.
    Solution - The command used was 
        nmap -sn 192.168.29.0/24

3. Command used to connect with the wifi
    Solution - 
        sudo nmcli dev wifi connect "wifiname" password "actual_password"
    Then we can get the ip using the command
        - ip addr show wlan0

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
