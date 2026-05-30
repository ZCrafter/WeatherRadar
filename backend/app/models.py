from sqlalchemy import Column, DateTime, Float, Integer, String, Text, func
from app.db import Base

class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, unique=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timezone = Column(String(80), nullable=False, default="auto")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ModelCatalog(Base):
    __tablename__ = "model_catalog"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, unique=True)
    provider = Column(String(120), nullable=False, default="Open-Meteo")
    enabled = Column(Integer, nullable=False, default=1)

class ForecastSnapshot(Base):
    __tablename__ = "forecast_snapshots"
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, nullable=False, index=True)
    model = Column(String(120), nullable=False, index=True)
    run_time = Column(DateTime(timezone=True), nullable=False, index=True)
    target_time = Column(DateTime(timezone=True), nullable=False, index=True)
    lead_minutes = Column(Integer, nullable=False, index=True)
    temperature_2m = Column(Float, nullable=True)
    precipitation = Column(Float, nullable=True)
    wind_speed_10m = Column(Float, nullable=True)
    raw_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Observation(Base):
    __tablename__ = "observations"
    id = Column(Integer, primary_key=True, index=True)
    location_id = Column(Integer, nullable=False, index=True)
    observed_time = Column(DateTime(timezone=True), nullable=False, index=True)
    temperature_2m = Column(Float, nullable=True)
    precipitation = Column(Float, nullable=True)
    wind_speed_10m = Column(Float, nullable=True)
    raw_json = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
