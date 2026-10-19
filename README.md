# CommitmentSync

Team beta — spec §3.2 hackathon build.

**One-liner:** CommitmentSync – the only AI‑driven, policy‑centric engine that automatically optimizes cross‑cloud reservations, with built‑in compliance tagging, staged approval, and sandbox testing to eliminate cost bleed and regulatory risk.

**Problem:** Enterprise teams waste $10‑$30M+ annually on over‑ or under‑committed compute across AWS, Azure, GCP, and on‑prem, because existing tools either cover one provider, lack unified governance, or expose them to costly mis‑adjustments with no regulatory audit support.

**Solution:** CommitmentSync ingests real‑time billing, usage, and reservation data via a unified SDK and provider APIs, then uses lightweight time‑series ML to forecast demand per workload cluster. A declarative policy language lets teams set cross‑cloud cost budgets, risk tolerances, and compliance tags (GDPR, HIPAA, FedRAMP). The system simulates financial impact, routes changes through a staged approval gate with provider‑specific compliance checklists, and offers a sandbox mode that clones billing data for safe testing. Approved reservation updates are automatically drafted and submitted across all clouds, while audit logs, compliance reports, and CI/CD hooks keep governance tight. Slack/Teams bots deliver real‑time alerts and simulation summaries to keep stakeholders informed without workflow disruption.

**Build scope:** **CommitmentSync – Day 4‑5 Architecture (≈ 180 words)**  

**Tech‑stack**  
- **Compute / Orchestration:** Kubernetes (EKS/GKE/AKS) with Argo Workflows for batch jobs.  
- **Ingestion & API layer:** Go micro‑services + gRPC; unified SDK built on Terraform Provider SDK for AWS, Azure, GCP, Oracle, VMware.  
- **Data store:** ClickHouse (high‑speed columnar) for raw billing/usage; Redis for forecast cache.  
- **ML forecasting:** Python (Prophet + PyTorch‑TS) served via TorchServe; auto‑scales with Keda.  
- **Policy & workflow engine:** Open Policy Agent (OPA) + Temporal.io for approval state‑machines.  
- **UI/CLI:** React + TypeScript front‑end, FastAPI‑based CLI.  
- **Notifications:** Slack/Teams bots via Bolt SDK; webhook endpoints for CI/CD.  

**Three core components**  
1. **Unified Ingestion Hub** – pulls billing, usage, and reservation data from all providers, normalises into a common schema, writes to ClickHouse.  
2. **Demand Forecast & Simulation Engine** – time‑series ML predicts workload capacity; Monte‑Carlo runs simulate reservation scenarios and cost impact.  
3. **Policy‑Driven Orchestration Layer** – OPA evaluates declarative JSON/YAML policies; Temporal workflows manage multi‑step approvals, generate provider‑specific reservation API calls, and write immutable audit logs to S3/Blob.  

**Top 2 Risks**  
- *Provider API drift*: breaking changes in AWS/Azure/GCP reservation APIs could halt automation. Mitigation – versioned SDK wrappers with automated contract tests.  
- *Forecast error cost*: Over‑optimistic forecasts may cause under‑commitment and spikes. Mitigation – conservative safety‑margin band and continuous back‑testing alerts.  

**Fallback Scope (if risks materialise)**
- Roll back to *batch‑only* mode: generate weekly CSV recommendation reports for manual execution.
- Replace live ML with rule‑based thresholds (e.g., 80 % utilization) while keeping unified ingestion and audit trail.

**How to Run**
1. Create virtual environment: `python3 -m venv venv`
2. Activate environment: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `python -m src.commitmentsync.main`
5. Access health endpoint: `GET http://localhost:8000/health`
6. Test optimization endpoint: `POST http://localhost:8000/optimize` with JSON payload
7. Access interactive API documentation (Swagger UI): `http://localhost:8000/docs`
8. Access alternative API documentation (ReDoc): `http://localhost:8000/redoc`

## Running with Docker

1. Build the Docker image: `docker build -t commitmentsync .`
2. Run the container: `docker run -p 8000:8000 commitmentsync`
3. Access the application at `http://localhost:8000`

Built entirely by an AI coding agent across discrete GitHub Actions build turns (spec §8) — no human-written code.