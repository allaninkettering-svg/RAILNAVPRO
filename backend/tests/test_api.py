from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient


def create_user(client: TestClient) -> int:
    response = client.post(
        "/users",
        json={
            "primary_traveller_name": "Allan",
            "carer_name": "Jane",
            "email": "allan@example.com",
            "home_station": "London Kings Cross",
            "disability_details": "Registered blind",
            "railcard_details": "Disabled Persons Railcard",
        },
    )
    assert response.status_code == 201, response.text
    return response.json()["id"]


def build_segment_payload(offset_hours: int = 0) -> dict:
    departure = datetime.now(timezone.utc) + timedelta(hours=offset_hours)
    arrival = departure + timedelta(hours=2)
    return {
        "sequence": offset_hours,
        "mode": "train",
        "origin": "London Kings Cross",
        "destination": "York",
        "departure_time": departure.isoformat(),
        "arrival_time": arrival.isoformat(),
        "operator": "LNER",
        "cost": 35.5,
        "currency": "GBP",
        "accessibility_features": "Assisted boarding",
    }


def test_create_and_retrieve_trip(client: TestClient) -> None:
    user_id = create_user(client)

    response = client.post(
        "/trips",
        json={
            "user_id": user_id,
            "title": "Weekend in York",
            "origin": "London Kings Cross",
            "destination": "York",
            "departure_time": (datetime.now(timezone.utc)).isoformat(),
            "arrival_time": (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat(),
            "total_cost": 71.0,
            "currency": "GBP",
            "segments": [build_segment_payload()],
            "accessibility_notes": "Assistance at York",
        },
    )
    assert response.status_code == 201, response.text
    trip = response.json()

    fetch = client.get(f"/trips/{trip['id']}")
    assert fetch.status_code == 200
    payload = fetch.json()
    assert payload["title"] == "Weekend in York"
    assert len(payload["segments"]) == 1
    assert payload["segments"][0]["mode"] == "train"


def test_trip_update_and_listing(client: TestClient) -> None:
    user_id = create_user(client)
    create_response = client.post(
        "/trips",
        json={
            "user_id": user_id,
            "title": "Scotland adventure",
            "origin": "Edinburgh",
            "destination": "Inverness",
            "departure_time": (datetime.now(timezone.utc)).isoformat(),
            "arrival_time": (datetime.now(timezone.utc) + timedelta(hours=4)).isoformat(),
            "total_cost": 120.0,
            "currency": "GBP",
            "segments": [build_segment_payload()],
        },
    )
    trip_id = create_response.json()["id"]

    update_response = client.put(
        f"/trips/{trip_id}",
        json={
            "title": "Highland Explorer",
            "segments": [build_segment_payload(offset_hours=1)],
        },
    )
    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["title"] == "Highland Explorer"
    assert updated["segments"][0]["sequence"] == 1

    list_response = client.get(f"/trips?user_id={user_id}")
    assert list_response.status_code == 200
    trips = list_response.json()
    assert len(trips) == 1
    assert trips[0]["title"] == "Highland Explorer"


def test_passenger_assist_payload(client: TestClient) -> None:
    user_id = create_user(client)
    trip_response = client.post(
        "/trips",
        json={
            "user_id": user_id,
            "title": "Paris",
            "origin": "London St Pancras",
            "destination": "Paris Gare du Nord",
            "departure_time": (datetime.now(timezone.utc)).isoformat(),
            "arrival_time": (datetime.now(timezone.utc) + timedelta(hours=3)).isoformat(),
            "total_cost": 200.0,
            "currency": "GBP",
            "segments": [build_segment_payload()],
        },
    )
    trip_id = trip_response.json()["id"]

    response = client.post(
        "/passenger-assist",
        json={
            "trip_id": trip_id,
            "assistance_required": "Meet at platform with ramp",
            "contact_number": "+44123456789",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["message"].startswith("Passenger Assist")
    assert payload["payload"]["traveller_name"] == "Allan"
