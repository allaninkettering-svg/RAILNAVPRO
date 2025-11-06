# RailNav Pro

Prototype implementation of the RailNav Pro backend service. The FastAPI application
supports accessible trip planning workflows, including:

- User profile storage with disability and railcard details
- Trip creation with multi-segment itineraries and accessibility metadata
- Passenger Assist auto-fill payload generation for easy form submission

## Backend quickstart

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest  # run the automated test suite
uvicorn railnav_backend.api:app --reload
```

The API exposes an OpenAPI schema at `http://127.0.0.1:8000/docs` with interactive
documentation.
