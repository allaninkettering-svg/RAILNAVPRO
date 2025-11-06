"""Integration tests for the FastAPI trip endpoints."""
from __future__ import annotations

from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def login(email: str = "allan@example.com") -> str:
    response = client.post("/auth/login", json={"email": email, "otp": "123456"})
    assert response.status_code == 200
    return response.json()["access_token"]


def test_create_and_list_trip() -> None:
    token = login()
    payload = {
        "title": "London to York",
        "segments": [
            {
                "mode": "train",
                "origin": "London Kings Cross",
                "destination": "York",
                "departure_time": (datetime.utcnow() + timedelta(days=1)).isoformat(),
                "arrival_time": (datetime.utcnow() + timedelta(days=1, hours=2)).isoformat(),
                "service_number": "LNER 123",
                "accessibility_notes": ["Level boarding"]
            }
        ],
        "fare": {
            "currency": "GBP",
            "total": 45.5,
            "components": ["Advance single", "Split ticket at Peterborough"],
        },
        "passenger_assist_requested": True,
        "notes": "Meet Jane at platform assistance desk",
    }
    response = client.post(
        "/trips",
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
    )
    assert response.status_code == 201
    trip_id = response.json()["trip_id"]

    list_response = client.get(
        "/trips", headers={"Authorization": f"Bearer {token}"}
    )
    assert list_response.status_code == 200
    trips = list_response.json()["trips"]
    assert len(trips) == 1
    assert trips[0]["trip_id"] == trip_id


def test_update_trip_toggle_assist() -> None:
    token = login("jane@example.com")

    # Create trip first
    create_response = client.post(
        "/trips",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Paris weekend",
            "segments": [
                {
                    "mode": "train",
                    "origin": "London St Pancras",
                    "destination": "Paris Gare du Nord",
                    "departure_time": datetime.utcnow().isoformat(),
                    "arrival_time": (datetime.utcnow() + timedelta(hours=2, minutes=15)).isoformat(),
                    "service_number": "Eurostar 9021",
                    "accessibility_notes": ["Assistance booked"],
                }
            ],
            "fare": {
                "currency": "EUR",
                "total": 120.0,
                "components": ["Return fare", "Wheelchair space"],
            },
        },
    )
    assert create_response.status_code == 201
    trip_id = create_response.json()["trip_id"]

    update_response = client.patch(
        f"/trips/{trip_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"passenger_assist_requested": True, "notes": "Need escort"},
    )
    assert update_response.status_code == 200
    body = update_response.json()
    assert body["passenger_assist_requested"] is True
    assert body["notes"] == "Need escort"
