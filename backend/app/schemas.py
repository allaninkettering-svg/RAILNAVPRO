"""Pydantic schemas for the RailNav Pro backend."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """Represents Allan's profile information stored in the backend."""

    user_id: str = Field(..., description="Stable identifier for the account")
    name: str = Field(..., description="Full name for personalised prompts")
    email: str = Field(..., description="Login and notification address")
    home_station: Optional[str] = Field(
        None, description="Preferred origin station for trip planning"
    )
    disability_id: Optional[str] = Field(
        None, description="DPRC or equivalent identifier used for discounts"
    )
    carer_name: Optional[str] = Field(None, description="Primary travel companion")


class FareBreakdown(BaseModel):
    """Describes how a fare was composed, including split tickets and passes."""

    currency: str = Field(default="GBP")
    total: float = Field(..., ge=0)
    components: List[str] = Field(
        default_factory=list,
        description="Human-readable explanation of how the fare was optimised",
    )


class TripSegment(BaseModel):
    """Single leg of a journey, supporting trains, buses, and flights."""

    mode: str = Field(..., description="transport mode: train, bus, or plane")
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    service_number: Optional[str] = None
    accessibility_notes: List[str] = Field(default_factory=list)


class TripPlan(BaseModel):
    """Composite trip created by the planning engine and saved to the cloud."""

    trip_id: str
    user_id: str
    title: str
    created_at: datetime
    segments: List[TripSegment]
    fare: FareBreakdown
    passenger_assist_requested: bool = False
    notes: Optional[str] = None


class TripCreateRequest(BaseModel):
    """Payload used by the web app to persist a trip."""

    title: str
    segments: List[TripSegment]
    fare: FareBreakdown
    passenger_assist_requested: bool = False
    notes: Optional[str] = None


class TripUpdateRequest(BaseModel):
    """Payload used to toggle assist or update notes."""

    passenger_assist_requested: Optional[bool] = None
    notes: Optional[str] = None


class TripListResponse(BaseModel):
    """Response wrapper for returning a user's saved trips."""

    trips: List[TripPlan]


class LoginRequest(BaseModel):
    """Simplified login request until full auth is implemented."""

    email: str
    otp: str


class LoginResponse(BaseModel):
    """Token stub used by the clients to authenticate API requests."""

    access_token: str
    token_type: str = "bearer"
    user: UserProfile
