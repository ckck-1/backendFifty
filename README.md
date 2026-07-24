# Project Fifty Backend

A domain-driven multi-agent climate intelligence platform built with **FastAPI**, **LangGraph**, and **Mistral AI**.

## Overview

This MVP utilizes 15 specialized agents across three domains (Rainfall, Sunshine & Heat, Climate Intelligence) to synthesize climate data, predict drought indices, and recommend actionable insights. The orchestration is powered by a sequential LangGraph state machine.

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

Check the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`

### Example Request
```bash
curl -X POST "http://localhost:8000/api/analyze" -H "Content-Type: application/json" -d '{"location": "Bugesera", "query": "Analyze drought risk"}'
```

## Architecture (MVP)

- **app/core/**: App configuration and database engine
- **app/api/**: FastAPI routes (`/analyze`, `/agents`)
- **app/domains/**: Agent definitions (Rainfall, Sunshine & Heat, Climate Intel)
- **app/orchestration/**: LangGraph engine (`graph.py`), orchestrator, and registry
- **app/tools/**: Langchain `@tool` functions (Weather, Satellite, GIS, etc.)
- **app/services/**: LLM clients and memory storage
