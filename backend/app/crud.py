from sqlalchemy.orm import Session
from app import models, schemas

DEFAULT_MODELS = [
    "ecmwf_ifs",
    "gfs_seamless",
    "icon_global",
    "gem_global",
    "meteofrance_arpege_world",
    "ukmo_global",
]

def init_models(db: Session):
    existing = {m.name for m in db.query(models.ModelCatalog).all()}
    for name in DEFAULT_MODELS:
        if name not in existing:
            db.add(models.ModelCatalog(name=name, provider="Open-Meteo", enabled=1))
    db.commit()

def list_locations(db: Session):
    return db.query(models.Location).order_by(models.Location.name.asc()).all()

def create_location(db: Session, location: schemas.LocationCreate):
    obj = models.Location(**location.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def delete_location(db: Session, location_id: int):
    obj = db.query(models.Location).filter(models.Location.id == location_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj

def list_models(db: Session):
    return db.query(models.ModelCatalog).order_by(models.ModelCatalog.name.asc()).all()

def list_snapshots(db: Session, location_id: int):
    return (
        db.query(models.ForecastSnapshot)
        .filter(models.ForecastSnapshot.location_id == location_id)
        .order_by(models.ForecastSnapshot.target_time.asc())
        .all()
    )

def add_snapshot(db: Session, snapshot: models.ForecastSnapshot):
    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)
    return snapshot

def add_observation(db: Session, obs: models.Observation):
    db.add(obs)
    db.commit()
    db.refresh(obs)
    return obs

def list_observations(db: Session, location_id: int):
    return (
        db.query(models.Observation)
        .filter(models.Observation.location_id == location_id)
        .order_by(models.Observation.observed_time.asc())
        .all()
    )
