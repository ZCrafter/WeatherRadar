import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.db import get_db, Base, engine
from app import crud, schemas, models
from app.openmeteo import fetch_model_snapshot
from app.scoring import mae, bias

router = APIRouter(prefix="/api")
Base.metadata.create_all(bind=engine)

@router.get("/locations", response_model=list[schemas.LocationRead])
def read_locations(db: Session = Depends(get_db)):
    return crud.list_locations(db)

@router.post("/locations", response_model=schemas.LocationRead)
def add_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    return crud.create_location(db, location)

@router.delete("/locations/{location_id}")
def remove_location(location_id: int, db: Session = Depends(get_db)):
    obj = crud.delete_location(db, location_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"deleted": location_id}

@router.get("/models", response_model=list[schemas.ModelRead])
def read_models(db: Session = Depends(get_db)):
    crud.init_models(db)
    return [
        schemas.ModelRead(name=m.name, provider=m.provider, enabled=bool(m.enabled))
        for m in crud.list_models(db)
    ]

@router.post("/snapshot/{location_id}")
async def snapshot_location(location_id: int, db: Session = Depends(get_db)):
    loc = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")

    crud.init_models(db)
    enabled_models = [m.name for m in crud.list_models(db) if m.enabled]
    created = 0

    for model_name in enabled_models:
        rows = await fetch_model_snapshot(loc.latitude, loc.longitude, loc.timezone, model_name)
        for row in rows:
            snap = models.ForecastSnapshot(
                location_id=loc.id,
                model=model_name,
                run_time=row["run_time"],
                target_time=row["target_time"],
                lead_minutes=row["lead_minutes"],
                temperature_2m=row["temperature_2m"],
                wind_speed_10m=row["wind_speed_10m"],
                precipitation=row["precipitation"],
                raw_json=json.dumps(row["raw_json"]),
            )
            crud.add_snapshot(db, snap)
            created += 1

    return {"location_id": loc.id, "created": created}

@router.get("/snapshots/{location_id}", response_model=list[schemas.SnapshotRead])
def snapshots(location_id: int, db: Session = Depends(get_db)):
    return crud.list_snapshots(db, location_id)

@router.post("/observations")
def add_observation(obs: schemas.ObservationCreate, db: Session = Depends(get_db)):
    obj = models.Observation(**obs.model_dump())
    crud.add_observation(db, obj)
    return {"ok": True}

@router.get("/comparison/{location_id}")
def comparison(location_id: int, db: Session = Depends(get_db)):
    snaps = crud.list_snapshots(db, location_id)
    obs = crud.list_observations(db, location_id)
    obs_map = {o.observed_time.replace(tzinfo=None): o for o in obs}
    by_model = {}

    for s in snaps:
        by_model.setdefault(s.model, {"temp_pred": [], "temp_obs": []})
        o = obs_map.get(s.target_time.replace(tzinfo=None))
        if o:
            by_model[s.model]["temp_pred"].append(s.temperature_2m)
            by_model[s.model]["temp_obs"].append(o.temperature_2m)

    result = []
    for model_name, vals in by_model.items():
        result.append({
            "model": model_name,
            "temp_mae": mae(vals["temp_pred"], vals["temp_obs"]),
            "temp_bias": bias(vals["temp_pred"], vals["temp_obs"]),
            "pairs": len(vals["temp_pred"]),
        })
    return sorted(result, key=lambda x: (x["temp_mae"] is None, x["temp_mae"] if x["temp_mae"] is not None else 1e9))
