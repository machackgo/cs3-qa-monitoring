# CS3-QA-Monitoring: MLOps Monitoring & Observability System

## 1. Project Overview

CS3-QA-Monitoring is a complete MLOps Case Study 3 deployment demonstrating course-scale MLOps monitoring and observability for containerized Question Answering services. This repository contains a fully integrated monitoring stack built from MLOps course requirements, combining two QA applications (API-based and local-model), Prometheus metrics collection, Grafana Cloud visualization, automated CI/CD deployment via GitHub Actions, and ngrok-based demo/public access.

The system deploys and monitors two Question Answering applications:

- **qa-api**: An API-based QA application that calls Hugging Face inference APIs
- **qa-local**: A local-model QA application running inference locally

Both services expose application-specific metrics that are scraped by Prometheus, aggregated, and forwarded to Grafana Cloud for centralized observability.

---

## 2. Problem Solved

This project addresses several MLOps and DevOps challenges:

- **Monitoring Multiple Services**: How to collect and aggregate metrics from multiple containerized applications
- **Metrics Collection & Forwarding**: Implementing Prometheus scraping and remote metrics forwarding to cloud platforms
- **System-Level Observability**: Capturing host-level metrics using node-exporter alongside application metrics
- **Deployment Automation**: Automating end-to-end deployment, verification, and health checks
- **Demo & Demonstration Access**: Exposing services securely for external access without direct VM exposure
- **CI/CD Integration**: Building self-hosted GitHub Actions runners within Dockerized environments
- **Centralized Visibility**: Creating a unified observability layer across multiple services

---

## 3. Monitoring & Observability Workflow

```text
QA Services (qa-api, qa-local)
    ↓ expose metrics endpoints

Metrics Endpoints
    - qa-api metrics
    - qa-local metrics

    ↓ Prometheus scrape every 5 seconds

Prometheus Central Collector
    + node-exporter system metrics

    ↓ remote_write protocol

Grafana Cloud Metrics Ingestion
    ↓

Inspection & Debugging
    ↓

ngrok-based Demo/Public Access
```

---

## 4. Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| QA Services | Python-based QA applications | API-based and local-model QA services |
| Containerization | Docker | Package services into reproducible containers |
| Orchestration | Docker Compose | Run multiple services together |
| Metrics Collection | Prometheus | Scrape application and system metrics |
| System Metrics | node-exporter | Collect host-level CPU, memory, disk, and system metrics |
| Cloud Observability | Grafana Cloud remote_write | Forward metrics for cloud-based ingestion and inspection |
| CI/CD | GitHub Actions | Automate deployment and verification workflow |
| Runner Infrastructure | Self-hosted GitHub Actions runner | Execute deployment automation in a controlled environment |
| Demo Access | ngrok | Provide temporary public/demo access to services |
| Configuration | YAML | Prometheus and Docker Compose configuration |

---

## 5. Key Features

- **Dual QA Applications**  
  Supports both API-based inference and local-model inference for comparison.

- **Application Metrics Collection**  
  QA services expose metrics endpoints that Prometheus can scrape.

- **System Metrics Collection**  
  node-exporter collects host-level system metrics.

- **Prometheus Monitoring**  
  Prometheus is configured with multiple scrape jobs and a 5-second scrape interval.

- **Grafana Cloud Integration**  
  Prometheus forwards metrics using `remote_write` for Grafana Cloud metrics ingestion.

- **Docker Compose Orchestration**  
  Monitoring services and QA applications can be coordinated through Docker Compose.

- **CI/CD Deployment Automation**  
  GitHub Actions workflow supports automated deployment and verification.

- **Self-Hosted Runner Support**  
  Includes configuration for a Dockerized self-hosted GitHub Actions runner.

- **ngrok-Based Demo/Public Access**  
  Supports demonstration access without permanently exposing the VM directly.

- **Port Mapping and Container Networking**  
  Uses host-to-container port mappings for multi-service VM hosting.

---

## 6. How to Run Locally

### Prerequisites

- Python 3.8+
- Docker
- Docker Compose
- Git
- Access to required model/API dependencies for the QA services

### Clone the Repository

```bash
git clone https://github.com/machackgo/cs3-qa-monitoring.git
cd cs3-qa-monitoring
```

### Install QA Service Dependencies

```bash
pip install -r qa-api/requirements.txt
pip install -r qa-local/requirements.txt
```

### Run QA Services Locally

See the `qa-api` and `qa-local` service directories for app-specific run commands.

Example local service targets may include:

```text
qa-api frontend
qa-api backend
qa-local frontend
qa-local backend
```

---

## 7. How to Run with Docker Compose

### Start the Monitoring Stack

Navigate to the monitoring directory:

```bash
cd monitoring
```

Configure Grafana Cloud credentials only as environment variables or secrets:

```bash
export GRAFANA_CLOUD_REMOTE_WRITE_URL="YOUR_GRAFANA_URL"
export GRAFANA_CLOUD_USERNAME="YOUR_GRAFANA_USERNAME"
export GRAFANA_CLOUD_API_TOKEN="YOUR_GRAFANA_API_TOKEN"
```

Start services:

```bash
docker-compose up -d
```

Check running containers:

```bash
docker-compose ps
```

### Access Monitoring Services

Internal service ports and host-to-container mappings are documented in the Docker Compose and deployment configuration files.

Example monitoring targets:

```text
Prometheus targets page:
http://localhost:[prometheus-port]/targets

QA API metrics:
http://localhost:[qa-api-metrics-port]/metrics

QA Local metrics:
http://localhost:[qa-local-metrics-port]/metrics
```

### Example Prometheus Queries

```promql
up{job="qa-api-backend"}
```

```promql
up{job="qa-local-backend"}
```

```promql
node_cpu_seconds_total
```

---

## 8. Skills Demonstrated

| Skill Area | What This Repository Demonstrates |
|---|---|
| Prometheus Monitoring | Configuring scrape jobs, scrape intervals, and remote_write |
| Metrics Architecture | Collecting application-level and system-level metrics |
| Docker Compose | Coordinating multi-service monitoring deployments |
| Grafana Cloud Integration | Forwarding Prometheus metrics for cloud ingestion |
| CI/CD Automation | Using GitHub Actions for deployment workflows |
| Self-Hosted Runner Setup | Running GitHub Actions through a controlled runner environment |
| System Observability | Combining node-exporter system metrics with application metrics |
| Container Networking | Managing service communication and host-to-container port mappings |
| MLOps Monitoring | Observability for machine learning / QA service deployments |
| Demo Access | Using ngrok-based tunneling for external demonstration access |

---

## 9. VeriBridge Proof Evidence

| Component / Skill | Evidence Location | Proof Details |
|---|---|---|
| Prometheus Configuration | `monitoring/prometheus.yml` | Prometheus configuration with scrape jobs |
| Scrape Interval | `monitoring/prometheus.yml` | Uses a 5-second scrape interval |
| QA-Local Metrics Endpoint | `monitoring/prometheus.yml` | Prometheus target for `qa-local-backend` metrics |
| QA-API Metrics Endpoint | `monitoring/prometheus.yml` | Prometheus target for `qa-api-backend` metrics |
| System Metrics | `monitoring/prometheus.yml` | node-exporter target for host-level metrics |
| Grafana Cloud Metrics Ingestion | `monitoring/prometheus.yml` | `remote_write` configuration |
| Docker Compose Orchestration | `monitoring/compose.yml` | Multi-service orchestration setup |
| CI/CD Automation | `.github/workflows/` | GitHub Actions workflow for deployment automation |
| Self-Hosted Runner | `github-runner/` | Dockerized runner configuration |
| QA API Service | `qa-api/` | API-based Question Answering service |
| QA Local Service | `qa-local/` | Local-model Question Answering service |
| Demo Access | ngrok-related configuration/docs if present | Supports temporary external access for demonstration |
| Containerized Monitoring | `monitoring/compose.yml` | Runs monitoring components as containers |

---

## 10. Recruiter Value & Skills

### Prometheus & Metrics Engineering

This repository shows hands-on ability to configure Prometheus, define scrape jobs, and collect metrics across multiple services.

### Grafana Cloud Integration

The project demonstrates how local or VM-hosted Prometheus metrics can be forwarded to Grafana Cloud using the `remote_write` protocol for cloud-based metrics ingestion.

### Docker & Container Orchestration

The monitoring stack uses Docker Compose to coordinate multiple services, networking, and metric collection targets.

### MLOps Monitoring Architecture

The project connects ML/QA services with observability infrastructure, showing understanding of how deployed AI services should be monitored.

### CI/CD & Deployment Automation

GitHub Actions workflows and self-hosted runner configuration demonstrate deployment automation skills.

### System-Level Observability

node-exporter integration shows the ability to monitor infrastructure health in addition to application-level metrics.

### Integration Engineering

This repository integrates multiple tools into one working monitoring workflow:

```text
QA services
→ metrics endpoints
→ Prometheus
→ node-exporter
→ Grafana Cloud remote_write
→ GitHub Actions
→ ngrok demo access
```

---

## 11. Future Improvements

- **Alerting Rules**  
  Add Prometheus alert rules for anomaly detection and automatic notifications.

- **Custom Grafana Dashboards**  
  Create custom dashboards for QA service latency, request count, error rate, and model-related metrics.

- **Log Aggregation**  
  Add structured log collection using ELK, Loki, or cloud logging.

- **Custom Application Metrics**  
  Add metrics such as inference latency, throughput, failed requests, token usage, and model response time.

- **Kubernetes Migration**  
  Move from Docker Compose to Kubernetes for larger-scale orchestration.

- **Advanced PromQL Queries**  
  Add more PromQL queries for service-level inspection.

- **SLO / SLA Tracking**  
  Define service-level objectives such as uptime and latency targets.

- **Long-Term Metrics Storage**  
  Configure long-term retention for historical monitoring analysis.

- **Automated Scaling**  
  Use metrics to inform scaling decisions in future deployments.

- **Dashboard Screenshots / Demo Walkthrough**  
  Add screenshots or a short demo showing the monitoring workflow.

---

## Repository Metadata

### Suggested GitHub Description

```text
MLOps monitoring and observability system for QA services using Docker Compose, Prometheus, Grafana Cloud remote_write, GitHub Actions, and ngrok demo access.
```

### Suggested GitHub Topics

```text
monitoring
prometheus
grafana
observability
mlops
docker-compose
github-actions
metrics-collection
devops
case-study
```

---

## Final Architecture Summary

This repository demonstrates a course-scale MLOps observability system with the following components:

- qa-api frontend and backend
- qa-local frontend and backend
- Prometheus metrics collector
- node-exporter system metrics
- Grafana Cloud metrics ingestion through `remote_write`
- GitHub Actions deployment automation
- Dockerized self-hosted runner
- ngrok demo/public tunneling

High-level flow:

```text
Users access QA service frontends
→ frontends communicate with service backends
→ backends expose metrics endpoints
→ Prometheus scrapes application metrics
→ node-exporter exposes system metrics
→ Prometheus forwards metrics to Grafana Cloud
→ GitHub Actions supports deployment automation
→ ngrok enables demo/public access
```

---

## Author

**Mohammed Mubashir Uddin Faraz**  
GitHub: [machackgo](https://github.com/machackgo)

---

