from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LocationCreate(BaseModel):
    name: str
    latitude: float
    longitude: float
    timezone: str = "auto"
    notes: Optional[str] = None

class LocationRead(LocationCreate):
    id: int

class ModelRead(BaseModel):
    name: str
    provider: str
    enabled: bool

class SnapshotRead(BaseModel):
    id: int
    location_id: int
    model: str
    run_time: datetime
    target_time: datetime
    lead_minutes: int
    temperature_2m: Optional[float] = None
    wind_speed_10m: Optional[float] = None
    precipitation: Optional[float] = None

class ObservationCreate(BaseModel):
    location_id: int
    observed_time: datetime
    temperature_2m: Optional[float] = None
    wind_speed_10m: Optional[float] = None
    precipitation: Optional[float] = None
