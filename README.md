# Project Fifty

Multi-agent climate intelligence platform powered by 50 specialised AI agents, CrewAI, and Mistral AI.

## Quick Start

### 1. Create virtual environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy the `.env` example and fill in your keys:

```bash
# Edit .env and set:
#   MISTRAL_API_KEY=your_key_here
#   DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/project_fifty
```

### 4. Create the PostgreSQL database

```bash
createdb project_fifty
```

Tables are created automatically on first startup.

### 5. Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6. Verify

```bash
curl http://localhost:8000/
# {"project":"Project Fifty","status":"running","version":"1.0.0"}

curl http://localhost:8000/health
# Full health check with agent count and DB status
```

## API Endpoints

| Method | Path         | Description                           |
|--------|--------------|---------------------------------------|
| GET    | `/`          | Project status ping                   |
| GET    | `/health`    | Full health check                     |
| GET    | `/api/agents`| List all 50 registered agents         |
| POST   | `/api/analyze`| Submit a climate analysis request    |

### POST /api/analyze

```json
{
  "location": "Bugesera",
  "query": "Analyze drought risk"
}
```

Response:

```json
{
  "location": "Bugesera",
  "risk_level": "SEVERE",
  "confidence": "0.82",
  "analysis": "...",
  "recommendations": ["...", "..."]
}
```

## Architecture

```
User Request
    ↓
FastAPI Endpoint
    ↓
Orchestrator Agent (selects relevant agents)
    ↓
CrewAI ClimateCrew (hierarchical workflow)
    ├─ Planning Agent
    ├─ Specialist Agents (dynamically selected)
    ├─ Decision Agent (synthesises results)
    └─ Report Generator Agent
    ↓
JSON Response
```

Only relevant agents are activated per request — the orchestrator uses keyword
matching to select the minimal required set from the 50-agent fleet.

## Agent Categories

| Category          | Agents | IDs   |
|-------------------|--------|-------|
| Orchestration     | 5      | 1–5   |
| Data Collection   | 10     | 6–15  |
| Climate Analysis  | 10     | 16–25 |
| AI Intelligence   | 10     | 26–35 |
| Human Impact      | 10     | 36–45 |
| Communication     | 5      | 46–50 |

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Settings from .env
│   ├── database.py          # SQLAlchemy async engine
│   ├── api/
│   │   ├── routes.py        # Router aggregation
│   │   └── analysis.py      # /api/analyze endpoint
│   ├── agents/
│   │   ├── registry.py      # 50 agent definitions
│   │   ├── factory.py       # AgentSpec → CrewAI Agent
│   │   ├── orchestrator.py  # Dynamic agent selection + pipeline
│   │   ├── data_agents.py
│   │   ├── climate_agents.py
│   │   ├── intelligence_agents.py
│   │   ├── impact_agents.py
│   │   └── communication_agents.py
│   ├── crews/
│   │   └── climate_crew.py  # CrewAI crew definition
│   ├── tools/
│   │   ├── weather_tool.py
│   │   ├── satellite_tool.py
│   │   ├── gis_tool.py
│   │   ├── database_tool.py
│   │   └── report_tool.py
│   ├── models/
│   │   ├── schemas.py       # Pydantic request/response models
│   │   └── database_models.py  # SQLAlchemy ORM models
│   ├── services/
│   │   ├── mistral.py       # Mistral AI client with retry
│   │   ├── memory.py        # Redis/in-memory context store
│   │   └── analysis_service.py
│   └── utils/
├── requirements.txt
├── .env
└── README.md
```
