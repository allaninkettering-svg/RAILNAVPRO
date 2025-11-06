"""FastAPI application exposing the RailNav backend."""
from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, database, models, schemas


def create_app() -> FastAPI:
    app = FastAPI(title="RailNav Pro Backend", version="0.1.0")

    @app.on_event("startup")
    def _create_tables() -> None:
        models.Base.metadata.create_all(bind=database.engine)

    @app.post("/users", response_model=schemas.UserProfileRead, status_code=status.HTTP_201_CREATED)
    def create_user(payload: schemas.UserProfileCreate, db: Session = Depends(database.get_session)):
        user = crud.create_user(db, payload)
        return user

    @app.get("/users/{user_id}", response_model=schemas.UserProfileRead)
    def read_user(user_id: int, db: Session = Depends(database.get_session)):
        user = crud.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    @app.put("/users/{user_id}", response_model=schemas.UserProfileRead)
    def update_user(
        user_id: int, payload: schemas.UserProfileUpdate, db: Session = Depends(database.get_session)
    ):
        user = crud.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return crud.update_user(db, user, payload)

    @app.get("/trips", response_model=list[schemas.TripRead])
    def list_trips(user_id: int | None = None, db: Session = Depends(database.get_session)):
        trips = crud.list_trips(db, user_id=user_id)
        return trips

    @app.post("/trips", response_model=schemas.TripRead, status_code=status.HTTP_201_CREATED)
    def create_trip(payload: schemas.TripCreate, db: Session = Depends(database.get_session)):
        user = crud.get_user(db, payload.user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        trip = crud.create_trip(db, payload)
        return trip

    @app.get("/trips/{trip_id}", response_model=schemas.TripRead)
    def read_trip(trip_id: int, db: Session = Depends(database.get_session)):
        trip = crud.get_trip(db, trip_id)
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
        return trip

    @app.put("/trips/{trip_id}", response_model=schemas.TripRead)
    def update_trip(trip_id: int, payload: schemas.TripUpdate, db: Session = Depends(database.get_session)):
        trip = crud.get_trip(db, trip_id)
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
        trip = crud.update_trip(db, trip, payload)
        return trip

    @app.delete("/trips/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_trip(trip_id: int, db: Session = Depends(database.get_session)):
        trip = crud.get_trip(db, trip_id)
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
        crud.delete_trip(db, trip)
        return None

    @app.post("/passenger-assist", response_model=schemas.PassengerAssistResponse)
    def passenger_assist(
        request: schemas.PassengerAssistRequest, db: Session = Depends(database.get_session)
    ):
        trip = crud.get_trip(db, request.trip_id)
        if not trip:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")

        payload = {
            "traveller_name": trip.user.primary_traveller_name,
            "carer_name": trip.user.carer_name,
            "journey_title": trip.title,
            "origin": trip.origin,
            "destination": trip.destination,
            "departure_time": trip.departure_time.isoformat(),
            "arrival_time": trip.arrival_time.isoformat(),
            "assistance_required": request.assistance_required,
            "contact_number": request.contact_number,
        }
        return schemas.PassengerAssistResponse(
            message="Passenger Assist form auto-fill prepared",
            payload=payload,
        )

    return app


app = create_app()
