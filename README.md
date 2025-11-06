# RailNav Pro

RailNav Pro is an accessible, cloud-synchronised travel companion that helps Allan and his carer Jane plan and execute complex multi-leg rail journeys.

This repository now includes:

- **FastAPI backend** (`backend/`): stores Allan's profile, supports trip sync, and exposes assist-aware endpoints for the web and Android clients.
- **Accessible React web planner** (`web/`): a WCAG-focused interface to create and save journeys with screen reader and voice support hooks.
- **Product proposal** (`PROPOSAL.md`): strategic overview and cost estimate for the broader MVP.

## Getting Started

### Backend API (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. It provides simplified login and trip CRUD endpoints that the web application consumes.

To execute automated tests:

```bash
cd backend
pytest
```

### Web Planner (Vite + React)

```bash
cd web
npm install
npm run dev
```

Set `VITE_API_BASE_URL` in a `.env` file if the backend is not running on the default `http://localhost:8000`.

The planner emphasises screen-reader clarity by using live regions, visible focus states, and semantic grouping. Saved trips are posted to the backend and will be available for future Android consumption.

## Next Steps

- Extend the backend persistence layer with a managed database and OAuth provider.
- Introduce WebSocket/FCM push notifications for real-time trip updates.
- Scaffold the Android companion to consume the same REST API and surface GPS-driven alerts.
