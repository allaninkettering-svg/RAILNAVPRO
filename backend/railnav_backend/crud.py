"""Data access helpers for the RailNav backend."""
from __future__ import annotations

from typing import Iterable, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas


def create_user(session: Session, payload: schemas.UserProfileCreate) -> models.UserProfile:
    user = models.UserProfile(**payload.dict())
    session.add(user)
    session.flush()
    return user


def get_user(session: Session, user_id: int) -> Optional[models.UserProfile]:
    return session.get(models.UserProfile, user_id)


def update_user(
    session: Session, user: models.UserProfile, payload: schemas.UserProfileUpdate
) -> models.UserProfile:
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(user, field, value)
    session.add(user)
    session.flush()
    return user


def list_trips(session: Session, user_id: Optional[int] = None) -> List[models.Trip]:
    stmt = select(models.Trip).order_by(models.Trip.departure_time)
    if user_id is not None:
        stmt = stmt.where(models.Trip.user_id == user_id)
    return list(session.scalars(stmt))


def get_trip(session: Session, trip_id: int) -> Optional[models.Trip]:
    return session.get(models.Trip, trip_id)


def _replace_segments(trip: models.Trip, segments: Iterable[schemas.TripSegmentCreate]) -> None:
    trip.segments.clear()
    for segment in segments:
        trip.segments.append(
            models.TripSegment(
                sequence=segment.sequence,
                mode=segment.mode,
                origin=segment.origin,
                destination=segment.destination,
                departure_time=segment.departure_time,
                arrival_time=segment.arrival_time,
                operator=segment.operator,
                cost=segment.cost,
                currency=segment.currency,
                accessibility_features=segment.accessibility_features,
            )
        )


def create_trip(session: Session, payload: schemas.TripCreate) -> models.Trip:
    trip = models.Trip(
        user_id=payload.user_id,
        title=payload.title,
        origin=payload.origin,
        destination=payload.destination,
        departure_time=payload.departure_time,
        arrival_time=payload.arrival_time,
        total_cost=payload.total_cost,
        currency=payload.currency,
        accessibility_notes=payload.accessibility_notes,
    )
    session.add(trip)
    session.flush()
    _replace_segments(trip, payload.segments)
    session.flush()
    return trip


def update_trip(
    session: Session, trip: models.Trip, payload: schemas.TripUpdate
) -> models.Trip:
    for field, value in payload.dict(exclude_unset=True, exclude={"segments"}).items():
        setattr(trip, field, value)
    if payload.segments is not None:
        _replace_segments(trip, payload.segments)
    session.add(trip)
    session.flush()
    return trip


def delete_trip(session: Session, trip: models.Trip) -> None:
    session.delete(trip)
    session.flush()
