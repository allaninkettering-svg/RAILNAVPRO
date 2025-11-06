"""FastAPI application acting as the RailNav Pro cloud backend MVP."""
from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .repository import store
from .schemas import (
    LoginRequest,
    LoginResponse,
    TripCreateRequest,
    TripListResponse,
    TripPlan,
    TripUpdateRequest,
    UserProfile,
)

app = FastAPI(
    title="RailNav Pro Cloud Backend",
    description=(
        "Accessible trip planning API providing sync between web and Android clients."
    ),
    version="0.1.0",
)

security = HTTPBearer(auto_error=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def authenticate(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> UserProfile:
    """Very small authentication stub until OAuth integration is ready."""

    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    user = store.get_user(credentials.credentials)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown token")
    return user


@app.post("/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest) -> LoginResponse:
    """Issues a deterministic token based on email for rapid prototyping."""

    token = f"token-{request.email}"
    profile = UserProfile(
        user_id=token,
        name="Allan" if request.email.startswith("allan") else request.email.split("@")[0].title(),
        email=request.email,
        home_station="London Kings Cross",
        disability_id="DPRC-123456",
        carer_name="Jane",
    )
    store.upsert_user(profile)
    return LoginResponse(access_token=token, user=profile)


@app.get("/profile", response_model=UserProfile)
async def get_profile(user: UserProfile = Depends(authenticate)) -> UserProfile:
    return user


@app.get("/trips", response_model=TripListResponse)
async def list_trips(user: UserProfile = Depends(authenticate)) -> TripListResponse:
    trips = store.list_trips(user.user_id)
    return TripListResponse(trips=trips)


@app.post("/trips", response_model=TripPlan, status_code=status.HTTP_201_CREATED)
async def create_trip(
    payload: TripCreateRequest, user: UserProfile = Depends(authenticate)
) -> TripPlan:
    trip = store.save_trip(
        user.user_id,
        title=payload.title,
        segments=payload.segments,
        fare=payload.fare,
        passenger_assist_requested=payload.passenger_assist_requested,
        notes=payload.notes,
    )
    return trip


@app.get("/trips/{trip_id}", response_model=TripPlan)
async def get_trip(trip_id: str, user: UserProfile = Depends(authenticate)) -> TripPlan:
    trip = store.get_trip(user.user_id, trip_id)
    if not trip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    return trip


@app.patch("/trips/{trip_id}", response_model=TripPlan)
async def update_trip(
    trip_id: str, payload: TripUpdateRequest, user: UserProfile = Depends(authenticate)
) -> TripPlan:
    updated = store.update_trip(
        user.user_id,
        trip_id,
        passenger_assist_requested=payload.passenger_assist_requested,
        notes=payload.notes,
    )
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")
    return updated
