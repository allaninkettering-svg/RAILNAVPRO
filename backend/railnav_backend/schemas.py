"""Pydantic schemas exposed via the API."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class TripSegmentBase(BaseModel):
    sequence: int = Field(..., ge=0)
    mode: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    operator: Optional[str] = None
    cost: float = Field(0, ge=0)
    currency: str = Field("GBP", min_length=3, max_length=3)
    accessibility_features: Optional[str] = None

    @validator("mode")
    def normalise_mode(cls, value: str) -> str:
        return value.lower()


class TripSegmentCreate(TripSegmentBase):
    pass


class TripSegmentRead(TripSegmentBase):
    id: int

    class Config:
        orm_mode = True


class TripBase(BaseModel):
    title: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    total_cost: float = Field(0, ge=0)
    currency: str = Field("GBP", min_length=3, max_length=3)
    accessibility_notes: Optional[str] = None


class TripCreate(TripBase):
    user_id: int
    segments: List[TripSegmentCreate] = []


class TripUpdate(BaseModel):
    title: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    departure_time: Optional[datetime] = None
    arrival_time: Optional[datetime] = None
    total_cost: Optional[float] = Field(default=None, ge=0)
    currency: Optional[str] = Field(default=None, min_length=3, max_length=3)
    accessibility_notes: Optional[str] = None
    segments: Optional[List[TripSegmentCreate]] = None


class TripRead(TripBase):
    id: int
    user_id: int
    segments: List[TripSegmentRead] = []

    class Config:
        orm_mode = True


class UserProfileBase(BaseModel):
    primary_traveller_name: str
    carer_name: Optional[str] = None
    email: Optional[str] = None
    home_station: Optional[str] = None
    disability_details: Optional[str] = None
    railcard_details: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(BaseModel):
    primary_traveller_name: Optional[str] = None
    carer_name: Optional[str] = None
    email: Optional[str] = None
    home_station: Optional[str] = None
    disability_details: Optional[str] = None
    railcard_details: Optional[str] = None


class UserProfileRead(UserProfileBase):
    id: int

    class Config:
        orm_mode = True


class PassengerAssistRequest(BaseModel):
    trip_id: int
    assistance_required: str
    contact_number: Optional[str] = None


class PassengerAssistResponse(BaseModel):
    message: str
    payload: dict
