import asyncio
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "backend"))

from app.db import SessionLocal, Base, engine
from app import crud, models
from app.openmeteo import build_snapshot_rows

Base.metadata.create_all(bind=engine)

LEAD_BUCKETS = [30, 60, 120, 180, 360, 720, 1440, 2880, 5760, 8640]

def save_snapshot(db, loc_id, model_name, row):
    snap = models.ForecastSnapshot(
        location_id=loc_id,
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

async def main():
    db = SessionLocal()
    try:
        crud.init_models(db)
        locations = crud.list_locations(db)
        models_enabled = [m.name for m in crud.list_models(db) if m.enabled]

        if not locations:
            print("No locations found.")
            return

        for loc in locations:
            print(f"Processing location: {loc.name}")
            for model_name in models_enabled:
                print(f"  Model: {model_name}")
                rows = await build_snapshot_rows(loc.latitude, loc.longitude, loc.timezone, model_name)
                count = 0
                for row in rows:
                    if row["lead_minutes"] < 0:
                        continue
                    if row["bucket_minutes"] not in LEAD_BUCKETS:
                        continue
                    save_snapshot(db, loc.id, model_name, row)
                    count += 1
                print(f"    saved {count} rows")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
