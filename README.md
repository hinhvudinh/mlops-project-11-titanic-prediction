# MLOps Project Guideline

This document provides a detailed, step-by-step guideline for managing the MLOps lifecycle. Each section outlines the required steps and includes recommendations to improve the process.

---

## 1. Project Introduction

### 1.1 Business Understanding
- **Objective:** Define the business problem and objectives.
- **Key Elements:**
  - Problem statement
  - Key performance indicators (KPIs)
  - Stakeholder analysis
- **Recommendations:**
  - Incorporate market research and user feedback.
  - Regularly update the business case as new insights emerge.

### 1.2 Overview
- **Objective:** Present a high-level summary of the project.
- **Key Elements:**
  - Project goals
  - Expected outcomes
  - Methodology overview
- **Recommendations:**
  - Create an executive summary for technical and non-technical stakeholders.
  - Use diagrams or flowcharts to visually represent the project process.

### 1.3 Pain-Points
- **Objective:** Identify and detail the current challenges.
- **Key Elements:**
  - List of challenges (e.g., inefficiencies, scalability issues)
  - Impact analysis on operations
- **Recommendations:**
  - Conduct stakeholder interviews to ensure comprehensive identification of pain points.
  - Prioritize issues based on impact and feasibility of resolution.

### 1.4 Target
- **Objective:** Define target outcomes and success metrics.
- **Key Elements:**
  - SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound)
  - Performance metrics
- **Recommendations:**
  - Set up periodic reviews to track progress.
  - Align targets with both business and technical objectives.

---

## 2. MLOps Workflow

### 2.1 Database Setup
- **Steps:**
  - **Using GCP GUI:**  
    - Create and configure the database instance.
    - Set up user access and permissions.
  - **Using CLI:**  
    - Utilize GCP Cloud SDK for command-line management.
    - Automate database setup scripts.
    - Use this cript to load data from kaggle to google cloud bucket
    ```bash
    # Step 1: Setup Kaggle
    mkdir -p ~/.kaggle
    echo '{your kaggle.json content here}' > ~/.kaggle/kaggle.json
    chmod 600 ~/.kaggle/kaggle.json

    # Step 2: Install kaggle CLI
    pip install kaggle --upgrade

    # Step 3: Download dataset (step 1, 2, 3 can be used in local computer to download data)
    kaggle datasets download -d zynicide/wine-reviews -p ./kaggle_data --unzip

    # Step 4: Upload to GCS
    export BUCKET_NAME=your-bucket-name
    gsutil -m cp -r ./kaggle_data/* gs://$BUCKET_NAME/kaggle_data/

    ```
- **Recommendations:**
  - Automate database backups and security updates.
  - Use Infrastructure as Code (IaC) tools (e.g., Terraform) for reproducibility.
  - Implement monitoring and alerting to catch issues early.
  - Add integration with data quality checks or anomaly detection jobs to alert on unexpected input data issues.

### 2.2 Project Setup

#### Project Structure
- **Directory Layout:**
  - **src:** Code for custom exceptions, data ingestion, preprocessing, logging, and model training.[1]
  - **artifacts:** Contains raw data, processed data, and model outputs.[1]
  - **config:**
    - `config`: Configuration files for data ingestion, data processing, etc.
    - `model_params`: Hyperparameters and tuning configurations.
    - `path_config`: File paths and directory settings.
  - **notebook:** Notebooks for testing, EDA, feature engineering, and initial modeling.
  - **pipeline:** Scripts to integrate data ingestion, preprocessing, and model training.[1]
  - **static:** Contains style assets like `style.css`.[1]
  - **templates:** HTML templates for user interfaces.[1]
  - **util:** Common functions (e.g., `load_data`, `read_yaml`).[1]
  - **Dockerfile:** Containerizes the project.
  - **Jenkinsfile:** Configures CI/CD processes.
  - **setup.py:** Project setup script.[1]
  - **requirements.txt:** Dependency list.[1]
  - **.gitignore:** Specifies files/directories to ignore in version control.[1]  
  [1] This is initial created project structure
  - *Setup project in setup.py, __init__.py in each folder contain .py, implement code for logger and exception, run setup environment*
- **Setup Environment:**
  ```bash
  python -m venv .venv
  pip install -e .
  ```
## Recommendations
- Consider write python script to generate project structure
- Document every folder and script with clear instructions.
- Keep code modular to facilitate testing and reuse.
- Automate environment setup and dependency management.
- Incorporate unit tests to verify module functionality.
- Use static code analysis tools like flake8, mypy, or pylint and integrate them into the CI process.
- Add a tests/ directory with pytest for automated testing.

---
## Data Engineering ETL Pipeline
- Using Airflow and PostgreSQL
- Install docker
- Setup astro:
  - In the CLI, dir project directory: astro init
  - Copy GCP-key to /include
  - add config
  ```yaml
    deployments:
    - name: dev
      executor: celery
      image:
        name: quay.io/astronomer/astro-runtime:7.3.0
      env: dev
      volumes:
        - ./include:/usr/local/airflow/include
  ```
  - Astro dockerfile
  ```Dockerfile
    FROM quay.io/astronomer/astro-runtime:12.8.0

    RUN pip install apache-airflow--providers-google
  ```
  - start Astro:
  ```bash
    astro dev start
  ```
- login to astro UI
  - user: admin
  - pw: admin

- setup gcp bucket, db postgres connection
  - admin tab/new record
  - detail in file project-materials/PROJECT-3 MATERIALS.txt
- create etl using python in dags/

## Recommendations
- Set up Airflow monitoring using Prometheus/Grafana or Astro UI to monitor DAG health. 
- Define SLA miss alerts to detect broken pipelines quickly.

---
## 2.3 Data Ingestion

### Steps
  - (manual) Load data from Kaggle
  - (manual) Load data from GCP bucket
  - Load data from database 
### Recommendations
- Add robust error handling and logging.
- Schedule periodic data validation to ensure data quality.
- Consider integrating data validation libraries like Great Expectations.
- Implement a retry mechanism for transient ingestion failures.
---

## 2.4 Jupyter Notebook Testing

### Steps
- **Data Loading:** Import and verify data integrity.
- **Preprocessing:** Clean and prepare data.
- **EDA:**
  - Analyze numerical and categorical variables.
  - Perform both single-variable and multi-variable analysis.
  - Apply feature engineering techniques (e.g., encoding categorical variables).
- **Model Training:** Develop and test initial models.
- **Hyper-Parameter Tuning:** Experiment with different settings.
[Notebook](./notebook/notebook.ipynb)
### Recommendations
- Use markdown cells to document each step.
- Version control notebooks to track changes.
- Convert successful notebook workflows into production-ready scripts.
- Use tools like nbstripout or jupytext to clean and version notebooks effectively.

---

## 2.5 Data Processing

### Steps
- Refactor the notebook code into reusable classes/functions for data processing.
- Load to feature store

### Recommendations
- Ensure scalability and modularity.
- Optimize performance (consider parallel processing if needed).
- Write comprehensive tests to validate transformations.
- Track data schema evolution using tools like pandera or great_expectations.

---

## 2.6 Model Training

### Steps
- Load features from feature store
- Refactor notebook-based model training into a class-based module.

### Recommendations
- Standardize the training process for easy performance comparisons.
- Use configuration files to manage experiment settings.
- Explore automated hyper-parameter tuning frameworks like Optuna.
- Validate input/output schema using libraries like pydantic for robustness.

---

## 2.7 Experiment Tracking

### Steps
- Use Tensorboard
  - Set up Tensorboard to track experiments, including parameters, metrics, and artifacts.
  - Start GUI
    ```bash
    tensorboard --logdir=tensorboard_logs/
    ```

- Use MLflow + Daghub (= Comet-ML)
  - Set up MLflow to track experiments, including parameters, metrics, and artifacts.

- Use Comet-ML
  - Setup account
  - See mlops-project-2/src/model_training.py

### Recommendations
- Configure MLflow with a robust storage backend.
- Regularly analyze experiment logs to identify trends.
- Create dashboards for real-time experiment monitoring.
- Use MLflow Model Registry to manage model lifecycle stages (Staging, Production).
- Standardize metadata (tags, versions) across tools like TensorBoard, Comet-ML, Mlflow
- Save model artifacts in cloud bucket like s3; google bucket

---

## 2.8 Training Pipeline

### Steps
- Use script
  - in pipeline/training_pipeline.py

- Use kubeflow for pipele orchestration
  - Install minikube/ enable docker kubernetes / kind, etc
  - Install kubeflow pipeline: https://www.kubeflow.org/docs/components/pipelines/legacy-v1/installation/localcluster-deployment/#2-creating-a-cluster-on-docker-desktop
  - Write script for kubeflow pipeline in kubeflow_pipeline/mlops_pipelines.py
  - Setup experiment + run
  - How to setup Kubeflow + MLflow?

### Recommendations
- Use workflow orchestration tools like Apache Airflow for scheduling.
- Ensure each pipeline component is modular for independent updates.
- Implement pipeline testing and rollback procedures.
- Automate pipeline validation (e.g., dry-run) before pushing changes.
- Use kfp.dsl.Condition and kfp.dsl.ExitHandler for robustness in Kubeflow pipelines.

---

## 2.9 Data Versioning

### Steps
- Establish a versioning system for datasets.
- DVC + GCP
- Create GCP bucket for dvc
- Install dvc in requirements.txt
  ```bash
    dvc init
    dvc add /artifacts/raw
    dvc add /artifacts/model
    dvc add /artifacts/model_checkpoint
    dvc add /artifacts/processed
    dvc add /artifacts/weights
    dvc status
  ```
  - track dvc to git
  ```git
    git status
    git add /artifacts
    git commit -m "add dvc"
    git push
  ```

  - add dvc data to gcp bucket
    - add dvc-gs to requirements.txt -> install
  ```bash
  dvc remote add -d mlops-prj2 gcs://your-bucket-name/path
  dvc remote modify mlops-prj2 credentialpath /path/to/gcs-key.json ! consider security best practice
  dvc status
  dvc push
  ```
  - to delete
  ```bash
  dvc remove /path/to/file.dvc
  dvc gc --workspace # to remove cached
  ```

### Recommendations
- Utilize tools such as DVC (Data Version Control) or Git-LFS.
- Maintain a changelog for data modifications.
- Integrate versioning into the CI/CD process for reproducibility.
- Automate DVC push/pull steps in Jenkins pipeline.
- Store gcs-key.json in a secret manager rather than plain text.

---

## 2.10 Code Versioning

### Steps
- Manage code using Git and host on GitHub.

### Recommendations
- Enforce code reviews and automated testing via pull requests.
- Adopt a branching strategy (e.g., Git Flow) for collaboration.
- Use continuous integration tools to maintain code quality.
- Integrate GitHub Actions or Jenkins for linting, testing, and security scans (e.g., bandit, trivy).

---

## 2.11 User App Building

### Steps
- API building and Testing using FastAPI, SwaggerUI and Postman
  - Install requirements in requirements.txt
  - Start app by using uvicorn main:app --reload
  - Testing using Postman or using http://localhost:8000/docs

### Recommendations
- Apply responsive design for an improved user experience.
- Implement API versioning to manage changes.
- Integrate user authentication and adhere to data security best practices.
- Add health/readiness/liveness probes if deploying with Kubernetes.
- Implement logging middleware and monitoring (e.g., Prometheus FastAPI exporter).

---

## 2.12 Monitoring and observation using Grafana + Prometheus
### Steps
- Using docker-compose to set up.
- Should use ChatGPT to get the recommend for the monitoring metrics.
- Start service using `docker compose up -d`.
- See the code in `application.py` to check the setup metrics.
- Visit Grafana HTTP endpoint → Connections → Data Sources.
- Use `http://{prometheus container name}:{port}` instead of `http://localhost:{port}`.
- In the Ubuntu env:
  - Check the IP: `ip addr show docker0`.
  - Check the Prometheus UI: `http://localhost:9090/targets` — targets should be in `UP` state.
  - `prometheus.yml` should be:
    ```yaml
    global:
      scrape_interval: 15s

    scrape_configs:
      - job_name: 'flask_app'
        static_configs:
          - targets: ['172.17.0.1:7978']  # on Windows/Mac use host.docker.internal
    ```

### Recommendations

- **Application Metrics:**
  - Use Prometheus-compatible exporters such as:
    - `prometheus_flask_exporter` or `prometheus-fastapi-instrumentator`.
    - Track API metrics like request latency, error rate, total requests, uptime.
    - Track ML-specific metrics like model confidence, prediction count, inference duration.

- **System Metrics:**
  - Integrate **Node Exporter** to monitor CPU, memory, disk usage on your server or VM.
  - Use **cAdvisor** to track Docker container resource usage and performance.

- **Pipeline Monitoring:**
  - For Airflow and Kubeflow pipelines:
    - Use `prometheus-pushgateway` to push custom pipeline metrics.
    - Add DAG/task success/failure counters.
    - Monitor DAG duration and SLAs.

- **Log Monitoring:**
  - Add **Loki + Grafana** stack for centralized, queryable logs.
  - Ensure FastAPI logs include structured JSON format for easier parsing and alerting.
  - Monitor `uvicorn` access logs and training logs.

- **Dashboarding:**
  - Build Grafana dashboards for:
    - System health (CPU, RAM, Disk from Node Exporter)
    - Docker/container metrics (cAdvisor)
    - App performance (request duration, throughput)
    - ML metrics (model accuracy, data drift indicators)
    - CI/CD status (Jenkins build times, deployment health)

- **Alerting:**
  - Set up **Prometheus Alertmanager**:
    - Create alert rules (e.g., 5xx spike, latency > 1s, memory > 90%, pipeline failed).
    - Send notifications via email, Slack, or Telegram.

- **Security & Access:**
  - Protect monitoring endpoints with:
    - Basic auth or OAuth2
    - HTTPS reverse proxy (e.g., NGINX or Caddy)
    - IP whitelisting for sensitive dashboards

- **Storage and Retention:**
  - Set Prometheus data retention policy to match disk limits:
    ```bash
    --storage.tsdb.retention.time=30d
    ```
  - Consider using **Thanos or Cortex** if you need long-term metrics storage.

- **Best Practices:**
  - Add a `/metrics` endpoint health check in your CI/CD pipeline.
  - Use `blackbox_exporter` to monitor service availability (ping, HTTP probe).
  - Export and version control Grafana dashboards as JSON (`infra as code`).
  - Use **Grafana Annotations** to mark events like deployments and retrainings on the charts.
---

## 2.13 CI/CD Deployment

### Steps

- Create VM machine
- Connect to instance via ssh
- Clone project
  - setup git credential
  ```bash
  git config --global user.name "hinhvudinh"
  git config --global user.email "rishavalenene@gmail.com"
  git config --global credential.helper store
  ```
- install docker and post install
- install minikube
- install kubectl
- install jenkins (note: in the same network as minikube)
  ```bash
  docker run -d --name jenkins \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(which docker):/usr/bin/docker \
  -u root \
  -e DOCKER_GID=$(getent group docker | cut -d: -f3) \
  --network minikube \
  jenkins/jenkins:lts
  ```
  - run: docker logs jenkins to get password
  - create firewall for jenkins (in production should limit port not all port)
  - install suggested plugin
  - install Docker, Docker pipeline, kubernetes plugin
  - reset Jenkins
  - follow 
  ```bash
  docker exec -it jenkins bash

  apt update -y
  apt install -y python3
  python3 --version
  ln -s /usr/bin/python3 /usr/bin/python
  python --version
  apt install -y python3-pip
  apt install -y python3-venv
  exit
  ```
  - restart jenkins: docker restart jenkins
  - jenkins github integration
    - create git token: repo; workflow; admin: org; admin:public_key; admin:repo_hook; admin:org_hook
    - setup github credential in jenkins: username with password:
      - ID: github-token
  - create pipeline use jenkinsfile
  - create docker repo
  - create docker token
  - create jenkins docker credentials with username/password
  - update jenkinsfile
  - setup ArgoCD
    - create namespace for argocd
    ```bash
    kubectl create ns argocd
    ```
    - install argocd
    ```bash
    kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
    # convert svc argocd-server to nodeport
    kubectl edit svc argocd-server -n argocd
    # change ClusterIP -> NodePort 
    kubectl port-forward --address 0.0.0.0 service/argocd-server 30367:80 -n argocd
    # access to port 30367 for argocd UI
    kubectl get secret -n argocd argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
    ```
  - config jenkins kubernetes
    on vm machine: cat .kube/config 
  - use notepad or vim or any text editor to change into:
    on code directory: ./kubeconfig

      by using
      cat /home/vdhinh/.minikube/ca.crt | base64 -w 0; echo
      cat /home/vdhinh/.minikube/profiles/minikube/client.crt | base64 -w 0; echo
      cat /home/vdhinh/.minikube/profiles/minikube/client.key | base64 -w 0; echo

      save the file as kubeconfig
  - at jenkins project pipeline:
    - Pipeline Syntax/kubeconfig: Setup Kubernetes CLI (kubectl)
    - get kubernetes server endpoint
    ```bash
    kubectl cluster-info
    ```
    - comeback to jenkinsfile
      - Install kubectl & argocd cli
    - setup argocd app
      - setup connection
      - setup application
        - Application Name: mlopsproj10 (note same as in ***argocd app sync*** in Jenkinsfile)
        - ...
        - Sync policy: Prune; self heal
        - repo
        - main
        - path: manifests
        - cluster url
        - namespace: argocd (can create another namespace ~~`)
  - access to the app; at vm machine
    ```bash
    minikube tunnel
    ```
    another terminal:
    ```bash
    kubectl port-forward svc/my-service -n argocd --address 0.0.0.0 9090:80
    ```
    - access vm_ip:9090
  
  - github webhook use jenkins url vm_ip:8080
  - in pipeline /setting check github hook trigger

### Recommendations
- Automate tests and deployments to minimize manual interventions.
- Implement robust monitoring and logging for production deployments.
- Consider blue-green or canary deployment strategies for smoother rollouts.
- Regularly update deployment scripts to incorporate the latest security practices.
- Add Prometheus/Grafana monitoring stack for deployed services.
- Store secrets (Docker tokens, GitHub credentials) in a secure vault or secret manager.
- Create a rollback pipeline in Jenkins for failed deployments.
- Add unit and integration test stages in Jenkins pipeline before deployment.

What is missing?
- Continuous training
- Frontend/backend