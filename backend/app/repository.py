"""In-memory persistence and mock AI orchestration for the MVP."""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from .schemas import FareBreakdown, TripPlan, TripSegment, UserProfile


class InMemoryStore:
    """Lightweight store to unblock client development before the real cloud backend."""

    def __init__(self) -> None:
        self._users: Dict[str, UserProfile] = {}
        self._trips: Dict[str, List[TripPlan]] = {}

    def upsert_user(self, profile: UserProfile) -> UserProfile:
        self._users[profile.user_id] = profile
        self._trips.setdefault(profile.user_id, [])
        return profile

    def get_user(self, user_id: str) -> Optional[UserProfile]:
        return self._users.get(user_id)

    def save_trip(
        self,
        user_id: str,
        title: str,
        segments: List[TripSegment],
        fare: FareBreakdown,
        passenger_assist_requested: bool = False,
        notes: Optional[str] = None,
    ) -> TripPlan:
        trip = TripPlan(
            trip_id=f"trip-{len(self._trips[user_id]) + 1}",
            user_id=user_id,
            title=title,
            created_at=datetime.utcnow(),
            segments=segments,
            fare=fare,
            passenger_assist_requested=passenger_assist_requested,
            notes=notes,
        )
        self._trips[user_id].append(trip)
        return trip

    def list_trips(self, user_id: str) -> List[TripPlan]:
        return list(self._trips.get(user_id, []))

    def update_trip(
        self,
        user_id: str,
        trip_id: str,
        *,
        passenger_assist_requested: Optional[bool] = None,
        notes: Optional[str] = None,
    ) -> Optional[TripPlan]:
        for idx, trip in enumerate(self._trips.get(user_id, [])):
            if trip.trip_id == trip_id:
                updated = trip.model_copy(update={
                    "passenger_assist_requested": passenger_assist_requested
                    if passenger_assist_requested is not None
                    else trip.passenger_assist_requested,
                    "notes": notes if notes is not None else trip.notes,
                })
                self._trips[user_id][idx] = updated
                return updated
        return None

    def get_trip(self, user_id: str, trip_id: str) -> Optional[TripPlan]:
        for trip in self._trips.get(user_id, []):
            if trip.trip_id == trip_id:
                return trip
        return None


store = InMemoryStore()
"""Module-level store instance shared by the FastAPI routes."""
