# CS3 QA Monitoring

This repository contains the complete MLOps Case Study 3 deployment for two Question Answering applications and their monitoring stack. It combines containerized application deployment, Prometheus-based metrics collection, Grafana Cloud visualization, a Dockerized self-hosted GitHub Actions runner, and public demo exposure using ngrok.

## Project Overview

This project deploys and monitors two QA systems:

- **qa-api** — an API-based Question Answering application that calls a Hugging Face inference API
- **qa-local** — a local-model Question Answering application that runs inference locally

The goal of the case study was not only to deploy both applications on a VM, but also to monitor them end to end, automate deployment with GitHub Actions, and demonstrate public accessibility outside the internal VM network.

## What This Repository Includes

This repository combines:

- `qa-api/` — API-based QA application
- `qa-local/` — local-model QA application
- `monitoring/` — Prometheus and node-exporter setup
- `github-runner/` — Dockerized self-hosted GitHub Actions runner
- `.github/workflows/` — CI/CD workflow for deploy-and-verify automation

## Final Architecture

The final deployed system includes:

- **qa-api frontend**
- **qa-api backend**
- **qa-local frontend**
- **qa-local backend**
- **Prometheus**
- **node-exporter**
- **Grafana Cloud remote_write integration**
- **Dockerized self-hosted GitHub Actions runner**
- **ngrok tunnels for external public access**

### High-level flow

1. Users access either `qa-api` or `qa-local`
2. Frontends communicate with their corresponding backends over the internal Docker network
3. Backends expose application metrics
4. Prometheus scrapes:
   - qa-api backend metrics
   - qa-local backend metrics
   - node-exporter metrics
5. Prometheus forwards metrics to Grafana Cloud using `remote_write`
6. GitHub Actions deploys and verifies the stack through a self-hosted runner on the VM
7. ngrok exposes the frontends publicly for external demonstration

---

# Final Host Port Mapping

## Reserved group04 host ports

| Service | Host Port |
|--------|----------:|
| qa-api frontend | 22080 |
| qa-local frontend | 22081 |
| qa-api backend | 22082 |
| qa-local backend | 22083 |
| qa-api metrics | 22084 |
| qa-local metrics | 22085 |
| Prometheus UI | 22086 |
| node-exporter | 22087 |
| qa-api ngrok reservation | 22088 |
| qa-local ngrok reservation | 22089 |

## Internal container ports

| Service | Internal Port |
|--------|--------------:|
| qa-api frontend | 7004 |
| qa-api backend | 9004 |
| qa-api metrics | 9101 |
| qa-local frontend | 7044 |
| qa-local backend | 9044 |
| qa-local metrics | 9104 |
| Prometheus | 9090 |
| node-exporter | 9100 |

---

# Repository Structure

```text
cs3-qa-monitoring/
├── .github/
│   └── workflows/
│       └── cs3-cicd.yml
├── github-runner/
│   └── compose.yml
├── monitoring/
│   ├── compose.yml
│   └── prometheus.yml
├── qa-api/
│   ├── backend/
│   ├── frontend/
│   └── compose.yml
├── qa-local/
│   ├── backend/
│   ├── frontend/
│   └── compose.yml
└── README.md
