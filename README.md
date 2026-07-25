# Project Fifty Backend

A domain-driven multi-agent climate intelligence platform built with **FastAPI**, **LangGraph**, and **Mistral AI**.

## Overview

This platform utilizes 50 specialized agents across three domains (Rainfall, Sunshine & Heat, Climate Intelligence) to synthesize climate data, predict drought indices, and recommend actionable insights. The orchestration is powered by a sequential LangGraph state machine.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   Copy `.env.example` to `.env` and fill in your keys.
   ```bash
   cp .env.example .env
   ```

3. **Start the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

## Usage

Interactive API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Example Request
```bash
curl -X POST "http://localhost:8000/api/analyze" -H "Content-Type: application/json" -d '{"location": "Bugesera", "query": "Analyze drought risk"}'
```

## Architecture

- **app/core/**: App configuration and database engine
- **app/api/**: FastAPI routes (`/analyze`, `/agents`, `/cabinet-briefs/*`)
- **app/domains/**: 50 agent definitions across 3 domains
  - `rainfall/` — 15 agents (data collection, deficit, anomalies, forecasting, impact)
  - `sunshine_heat/` — 15 agents (solar, temperature, crop stress, evaporation, human risk)
  - `climate_intel/` — 20 agents (trends, scoring, prediction, recommendations, reporting)
- **app/orchestration/**: LangGraph engine, orchestrator, registry, factory
- **app/tools/**: Langchain `@tool` functions (Weather via NASA POWER, Satellite, GIS, etc.)
- **app/services/**: Mistral AI client, memory, NASA POWER, ArcGIS, APScheduler

## Data Sources

| Source | Status | Used For |
|--------|--------|----------|
| NASA POWER API | Live | Temperature, solar radiation, humidity, precipitation, wind |
| ArcGIS Feature Layer | Live | Dashboard push (30 sectors loaded) |
| Mistral AI | Live | Agent LLM reasoning |
| CHIRPS rainfall | Deferred | Better precipitation data — planned for v2 |
| MODIS/NDVI | Deferred | Vegetation health — planned for v2 |
| GRACE groundwater | Deferred | Groundwater anomaly — planned for v2 |

## Key Features

- **50-agent pipeline** covering drought, heat, and climate intelligence
- **Cabinet Approval Gate** (FR-15/AC-07): safety-critical approval workflow before dispatch
- **Real-time data** from NASA POWER API for 30 Rwandan sectors
- **ArcGIS integration** for dashboard visualization
- **Daily scheduled pipeline** via APScheduler (06:00 RST)
- **Alembic migrations** for database schema management

## Testing

```bash
python -m pytest tests/ -v
```

## Deployment

See Render configuration in deployment docs. Requires:
- PostgreSQL database
- Environment variables for Mistral AI, ArcGIS, Twilio, NASA POWER
- `alembic upgrade head` for database migrations
