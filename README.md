Set-Content -Path "README.md" -Value '# Kasi-Logistics 🛵📦

> **Meta Global AI Developer Hackathon** — Indie Developer Track  
> Intelligent, capacity-constrained delivery routing and spatial segmentation designed for African township and informal settlement (Kasi) commerce.

---

## 🚀 Overview

**Kasi-Logistics** is a localized logistics optimization backend built to empower township spaza shops, local merchants, and independent delivery couriers. Traditional routing engines fail in dense, informal townships due to unmapped roads, lack of formal addresses, and varying vehicle capacity constraints. 

Kasi-Logistics solves this by combining:
1. **SAM 3.1 Spatial Segmentation Agent:** Processes geographic and visual data to cluster delivery nodes and identify optimal routing corridors within informal township layouts.
2. **Capacity-Constrained Nearest-Neighbor Optimizer:** Dynamically sequences multi-stop delivery routes while strictly adhering to vehicle weight limits and reducing fuel burn.
3. **Secure FastAPI Core:** High-performance, authenticated microservice with robust test coverage and automated CI/CD.

---

## 🛠️ Tech Stack & Architecture

- **Backend Framework:** FastAPI (Python 3.12)
- **Validation & Serialization:** Pydantic v2
- **Spatial Agent & Routing:** Custom Python algorithms incorporating SAM 3.1 spatial segmentation & capacity-constrained heuristics
- **Testing & Quality Assurance:** Pytest, HTTPX, Ruff linter
- **CI/CD:** GitHub Actions (automated testing & linting on push)

---

## 📂 Project Structure

```text
kasi-logistics/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application & endpoints (/health, /v1/routes/optimize)
│   ├── security.py          # Bearer token authentication & security middleware
│   └── agent/
│       ├── __init__.py
│       ├── optimizer.py     # Capacity-constrained route optimization engine
│       └── spatial.py       # SAM 3.1 spatial segmentation agent
├── tests/
│   ├── __init__.py
│   └── test_api.py          # Comprehensive pytest suite
├── .github/
│   └── workflows/
│       └── ci.yml           # Automated CI/CD pipeline
├── requirements.txt         # Project dependencies
└── README.md