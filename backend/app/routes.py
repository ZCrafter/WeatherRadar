import json
from datetime import datetime, timedelta, timezone
from collections import defaultdict

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db, Base, engine
from app import crud, schemas, models
from app.openmeteo import build_snapshot_rows, build_observation_rows
from app.scoring import mean_absolute_error, mean_bias, precipitation_brier_score, precipitation_hit_rate

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
        try:
            rows = await build_snapshot_rows(loc.latitude, loc.longitude, loc.timezone, model_name)
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
        except Exception:
            continue

    return {"location_id": loc.id, "created": created}

@router.post("/backfill/observations")
async def backfill_observations(days_back: int = 14, db: Session = Depends(get_db)):
    created = 0
    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=days_back)
    for loc in crud.list_locations(db):
        try:
            rows = await build_observation_rows(loc.latitude, loc.longitude, loc.timezone, start.isoformat(), end.isoformat())
            for row in rows:
                obs = models.Observation(
                    location_id=loc.id,
                    observed_time=row["observed_time"],
                    temperature_2m=row["temperature_2m"],
                    wind_speed_10m=row["wind_speed_10m"],
                    precipitation=row["precipitation"],
                    raw_json=json.dumps(row["raw_json"]),
                )
                crud.add_observation(db, obs)
                created += 1
        except Exception:
            continue
    return {"created": created}

@router.get("/comparison/{location_id}")
def comparison(location_id: int, db: Session = Depends(get_db)):
    snaps = crud.list_snapshots(db, location_id)
    obs_map = crud.get_observation_map(db, location_id)

    lead_buckets = [30, 60, 120, 180, 360, 720, 1440, 2880, 5760, 8640]

    grouped = defaultdict(lambda: defaultdict(lambda: {
        "temp_pred": [],
        "temp_obs": [],
        "precip_pred": [],
        "precip_obs": [],
        "series": []
    }))

    for s in snaps:
        obs = obs_map.get(s.target_time.replace(tzinfo=None))
        if not obs:
            continue
        bucket = min(lead_buckets, key=lambda x: abs(x - s.lead_minutes))
        g = grouped[s.model][bucket]
        g["temp_pred"].append(s.temperature_2m)
        g["temp_obs"].append(obs.temperature_2m)
        g["precip_pred"].append(s.precipitation)
        g["precip_obs"].append(obs.precipitation)
        g["series"].append({
            "target_time": s.target_time.isoformat(),
            "lead_minutes": s.lead_minutes,
            "temp_error": round((s.temperature_2m - obs.temperature_2m), 2) if s.temperature_2m is not None and obs.temperature_2m is not None else None,
            "precip_error": round((s.precipitation - obs.precipitation), 2) if s.precipitation is not None and obs.precipitation is not None else None,
            "temp_pred": round(s.temperature_2m, 2) if s.temperature_2m is not None else None,
            "temp_obs": round(obs.temperature_2m, 2) if obs.temperature_2m is not None else None,
            "precip_pred": round(s.precipitation, 2) if s.precipitation is not None else None,
            "precip_obs": round(obs.precipitation, 2) if obs.precipitation is not None else None,
        })

    result = []
    for model_name, by_bucket in grouped.items():
        buckets = []
        all_temp_pred = []
        all_temp_obs = []
        all_precip_pred = []
        all_precip_obs = []
        series = []
        for bucket in lead_buckets:
            g = by_bucket.get(bucket)
            if not g:
                continue
            all_temp_pred.extend(g["temp_pred"])
            all_temp_obs.extend(g["temp_obs"])
            all_precip_pred.extend(g["precip_pred"])
            all_precip_obs.extend(g["precip_obs"])
            series.extend(g["series"])
            buckets.append({
                "lead_minutes": bucket,
                "temp_mae": mean_absolute_error(g["temp_pred"], g["temp_obs"]),
                "temp_bias": mean_bias(g["temp_pred"], g["temp_obs"]),
                "precip_brier": precipitation_brier_score(g["precip_pred"], g["precip_obs"]),
                "precip_hit_rate": precipitation_hit_rate(g["precip_pred"], g["precip_obs"]),
                "pairs": len(g["temp_pred"]),
            })

        result.append({
            "model": model_name,
            "overall": {
                "temp_mae": mean_absolute_error(all_temp_pred, all_temp_obs),
                "temp_bias": mean_bias(all_temp_pred, all_temp_obs),
                "precip_brier": precipitation_brier_score(all_precip_pred, all_precip_obs),
                "precip_hit_rate": precipitation_hit_rate(all_precip_pred, all_precip_obs),
                "pairs": len(all_temp_pred),
            },
            "buckets": buckets,
            "series": sorted(series, key=lambda x: x["target_time"]),
        })

    return sorted(result, key=lambda x: (x["overall"]["temp_mae"] is None, x["overall"]["temp_mae"] if x["overall"]["temp_mae"] is not None else 1e9))
