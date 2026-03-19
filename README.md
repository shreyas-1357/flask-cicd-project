# 🚀 Flask CI/CD Pipeline — EC2 + EKS

> **Production-grade CI/CD pipeline on AWS** — from a GitHub push to a live Kubernetes deployment, fully automated with Jenkins, Docker, Amazon ECR, and EKS.

---

## 📌 Project Overview

This project implements a **complete end-to-end CI/CD pipeline** for a Python Flask application deployed on AWS. Every code push to GitHub automatically triggers a Jenkins pipeline that tests, builds, and deploys the application to an Amazon EKS (Kubernetes) cluster — with zero manual intervention.

Built as a **resume-grade DevOps project** demonstrating real-world skills used in production environments.

---

## 🏗️ Architecture

```
Developer (Local Machine)
        │
        │  git push
        ▼
   ┌─────────────┐
   │   GitHub    │  ──── webhook trigger ────▶  ┌─────────────────────┐
   └─────────────┘                              │   Jenkins on EC2    │
                                                │                     │
                                                │  1. Checkout code   │
                                                │  2. Run pytest      │
                                                │  3. Build image     │
                                                │  4. Trivy scan      │
                                                │  5. Push to ECR     │
                                                │  6. Helm deploy     │
                                                │  7. Verify pods     │
                                                └────────┬────────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────────┐
                                                │   Amazon ECR        │
                                                │  (Image Registry)   │
                                                └────────┬────────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────────┐
                                                │   Amazon EKS        │
                                                │  (Kubernetes)       │
                                                │                     │
                                                │  ┌───┐ ┌───┐ ┌───┐ │
                                                │  │Pod│ │Pod│ │Pod│ │
                                                │  └───┘ └───┘ └───┘ │
                                                └────────┬────────────┘
                                                         │
                                                         ▼
                                                ┌─────────────────────┐
                                                │  AWS Load Balancer  │
                                                │  (Public Endpoint)  │
                                                └─────────────────────┘
                                                         │
                                                         ▼
                                                  🌐 Flask App Live
```

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Application** | Python 3.11 + Flask 3.0 | Web application |
| **Testing** | Pytest + pytest-flask | Unit testing in CI |
| **Containerization** | Docker | Build and package app |
| **Registry** | Amazon ECR | Private Docker image registry |
| **CI Server** | Jenkins (on EC2) | Pipeline orchestration |
| **Orchestration** | Amazon EKS | Managed Kubernetes cluster |
| **K8s Packaging** | Helm 3 | Kubernetes manifest templating |
| **IaC** | Terraform | Infrastructure provisioning |
| **Security** | Trivy | Docker image vulnerability scanning |
| **Monitoring** | Prometheus + Grafana | Metrics and dashboards |
| **Version Control** | GitHub | Source of truth + webhook trigger |

---

## 📁 Project Structure

```
flask-cicd-project/
│
├── app/
│   ├── app.py                    # Flask application (3 endpoints)
│   ├── requirements.txt          # Python dependencies
│   └── tests/
│       ├── __init__.py
│       └── test_app.py           # Pytest unit tests (4 tests)
│
├── Dockerfile                    # Multi-stage container build
│
├── Jenkinsfile                   # 7-stage pipeline as code
│
├── helm/
│   └── flask-app/
│       ├── Chart.yaml            # Helm chart metadata
│       ├── values.yaml           # Default configuration values
│       └── templates/
│           ├── deployment.yaml   # K8s Deployment manifest
│           ├── service.yaml      # K8s Service (LoadBalancer)
│           └── ingress.yaml      # K8s Ingress rules
│
├── k8s/
│   ├── namespace.yaml            # Kubernetes namespace
│   └── configmap.yaml            # App configuration
│
└── README.md
```

---

## 🔄 CI/CD Pipeline Stages

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  1.Checkout  │───▶│  2. Tests    │───▶│  3. Build    │───▶│  4. Scan     │
│              │    │   (pytest)   │    │   (Docker)   │    │   (Trivy)    │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
                                                                     │
┌──────────────┐    ┌──────────────┐    ┌──────────────┐            │
│  7. Verify   │◀───│  6. Deploy   │◀───│  5. Push     │◀───────────┘
│    (K8s)     │    │   (Helm)     │    │   (ECR)      │
└──────────────┘    └──────────────┘    └──────────────┘
```

| Stage | What Happens | Failure Action |
|-------|-------------|----------------|
| **Checkout** | Pull latest code from GitHub | Stop pipeline |
| **Tests** | Run all pytest unit tests | Stop — nothing deploys if tests fail |
| **Build** | `docker build` with build number tag | Stop pipeline |
| **Security Scan** | Trivy scans for HIGH/CRITICAL CVEs | Warn and continue |
| **Push to ECR** | Push versioned image to Amazon ECR | Stop pipeline |
| **Deploy** | `helm upgrade --install` to EKS | Auto-rollback on failure |
| **Verify** | `kubectl rollout status` check | Alert if unhealthy |

---

## 🌐 API Endpoints

| Endpoint | Method | Response | Purpose |
|----------|--------|----------|---------|
| `/` | GET | `{"message": "...", "status": "healthy", "version": "..."}` | Main response |
| `/health` | GET | `{"status": "ok"}` | Kubernetes liveness probe |
| `/version` | GET | `{"version": "1.0.0"}` | Deployment version check |

---

## 🚀 Quick Start

### Prerequisites

Make sure you have these installed:
```bash
aws --version        # AWS CLI v2
kubectl version      # v1.29+
helm version         # v3+
eksctl version       # latest
docker --version     # v24+
git --version        # any recent version
```

### 1. Clone the repository
```bash
git clone https://github.com/shreyas-1357/flask-cicd-project.git
cd flask-cicd-project
```

### 2. Run Flask app locally
```bash
pip install -r app/requirements.txt
cd app && python app.py
# Visit http://localhost:5000
```

### 3. Run tests
```bash
python -m pytest app/tests/ -v
```

### 4. Build Docker image
```bash
docker build -t flask-cicd-app:latest .
docker run -p 5000:5000 flask-cicd-app:latest
```

---

## ☁️ AWS Infrastructure Setup

### Step 1 — Create EKS Cluster
```bash
eksctl create cluster \
  --name flask-cicd-cluster \
  --region us-east-1 \
  --nodegroup-name flask-nodes \
  --node-type t3.medium \
  --nodes 2 \
  --nodes-min 1 \
  --nodes-max 3 \
  --managed
```

### Step 2 — Create ECR Repository
```bash
aws ecr create-repository \
  --repository-name flask-cicd-app \
  --region us-east-1
```

### Step 3 — Configure kubectl for EKS
```bash
aws eks update-kubeconfig \
  --name flask-cicd-cluster \
  --region us-east-1
kubectl get nodes
```

### Step 4 — Deploy manually via Helm
```bash
helm upgrade --install flask-app ./helm/flask-app \
  --namespace flask-app \
  --create-namespace \
  --set image.repository=<ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/flask-cicd-app \
  --set image.tag=latest
```

---

## 🔧 Jenkins Setup on EC2

### Required Plugins
- Docker Pipeline
- GitHub Integration
- Kubernetes CLI
- Blue Ocean

### Required Credentials (Jenkins → Manage → Credentials)

| Credential ID | Type | Value |
|--------------|------|-------|
| `ecr-credentials` | AWS credentials | IAM user with ECR access |
| `github-token` | Secret text | GitHub personal access token |
| `kubeconfig` | Secret file | EKS kubeconfig file |

### Trigger Pipeline
The pipeline auto-triggers on every push to `main` via GitHub webhook.

Manual trigger:
```
Jenkins Dashboard → flask-cicd-pipeline → Build Now
```

---

## 📊 Monitoring

### Access Grafana Dashboard
```bash
kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring
# Visit http://localhost:3000
# Credentials: admin / admin123
```

### Key Metrics Tracked
- Pod CPU and memory usage
- HTTP request rate per endpoint
- Deployment rollout status
- Failed pod restarts

---

## 💰 AWS Cost Estimate

| Resource | Daily Cost | Monthly Cost |
|----------|-----------|--------------|
| EKS Control Plane | ~$2.40 | ~$72 |
| EC2 Worker Nodes (2x t3.medium) | ~$2.00 | ~$60 |
| EC2 Jenkins Server (t3.medium) | ~$1.00 | ~$30 |
| Load Balancer | ~$0.50 | ~$15 |
| ECR Storage | ~$0.01 | ~$0.30 |
| **Total** | **~$6/day** | **~$177/month** |

> ⚠️ Stop EC2 instances and delete the EKS cluster when not in use to avoid unnecessary charges.

---

## 🔁 Rollback Strategy

### Automatic Rollback
If the Jenkins pipeline fails at the Deploy or Verify stage, the `post { failure }` block automatically runs:
```bash
helm rollback flask-app -n flask-app
```

### Manual Rollback
```bash
# View release history
helm history flask-app -n flask-app

# Rollback to specific revision
helm rollback flask-app <revision> -n flask-app

# Or rollback Kubernetes deployment directly
kubectl rollout undo deployment/flask-app -n flask-app
```

---

## 🎤 Interview Talking Points

**Q: What happens if tests fail?**
Pipeline stops at Stage 2. Nothing gets built or deployed. The broken code never reaches the cluster.

**Q: How are Docker images versioned?**
Every image is tagged with the Jenkins `BUILD_NUMBER` — fully traceable back to the exact pipeline run and Git commit.

**Q: How do you handle secrets in Jenkins?**
AWS credentials and kubeconfig are stored as Jenkins credentials — never hardcoded in the Jenkinsfile. They are injected at runtime using `withCredentials{}` blocks.

**Q: How do you roll back a bad deployment?**
The Jenkinsfile `post { failure }` block automatically runs `helm rollback`. For manual rollbacks, `helm history` shows all previous releases and `helm rollback <revision>` restores any previous state in seconds.

**Q: Why Helm instead of raw kubectl apply?**
Helm gives us templating (one chart, configurable per environment), release history, atomic upgrades, and one-command rollbacks — none of which raw YAML gives you.

**Q: Why ECR instead of DockerHub?**
ECR is private by default, integrates with IAM for authentication (no passwords), lives in the same AWS network as EKS (faster pulls), and has automatic image scanning built in.

---

## 📈 Project Progress

- [x] Day 1 — Flask app with tests, GitHub repo
- [ ] Day 2 — Dockerfile + Amazon ECR
- [ ] Day 3 — EKS cluster setup
- [ ] Day 4 — Jenkins on EC2
- [ ] Day 5 — Full Jenkinsfile pipeline
- [ ] Day 6 — GitHub webhook auto-trigger
- [ ] Day 7 — Prometheus + Grafana monitoring

---

## 👤 Author

**Shreyas** — AWS & DevOps Engineer in Training

[![GitHub](https://img.shields.io/badge/GitHub-shreyas--1357-black?logo=github)](https://github.com/shreyas-1357)

---

## 📄 License

This project is for educational and portfolio purposes.
