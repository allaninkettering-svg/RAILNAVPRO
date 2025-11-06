"""SQLAlchemy models describing the RailNav domain."""
from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    primary_traveller_name: Mapped[str] = mapped_column(String(128), nullable=False)
    carer_name: Mapped[Optional[str]] = mapped_column(String(128))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    home_station: Mapped[Optional[str]] = mapped_column(String(128))
    disability_details: Mapped[Optional[str]] = mapped_column(Text)
    railcard_details: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False), default=datetime.utcnow, nullable=False
    )

    trips: Mapped[List["Trip"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Trip(Base):
    __tablename__ = "trips"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    origin: Mapped[str] = mapped_column(String(128), nullable=False)
    destination: Mapped[str] = mapped_column(String(128), nullable=False)
    departure_time: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    arrival_time: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    total_cost: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String(3), default="GBP")
    accessibility_notes: Mapped[Optional[str]] = mapped_column(Text)

    user: Mapped[UserProfile] = relationship(back_populates="trips")
    segments: Mapped[List["TripSegment"]] = relationship(
        back_populates="trip", cascade="all, delete-orphan", order_by="TripSegment.sequence"
    )


class TripSegment(Base):
    __tablename__ = "trip_segments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id", ondelete="CASCADE"))
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    mode: Mapped[str] = mapped_column(String(32), nullable=False)
    operator: Mapped[Optional[str]] = mapped_column(String(128))
    origin: Mapped[str] = mapped_column(String(128), nullable=False)
    destination: Mapped[str] = mapped_column(String(128), nullable=False)
    departure_time: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    arrival_time: Mapped[datetime] = mapped_column(DateTime(timezone=False))
    cost: Mapped[float] = mapped_column(Float, default=0.0)
    currency: Mapped[str] = mapped_column(String(3), default="GBP")
    accessibility_features: Mapped[Optional[str]] = mapped_column(Text)

    trip: Mapped[Trip] = relationship(back_populates="segments")
