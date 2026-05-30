import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.db import SessionLocal, Base, engine
from app import crud, models
from app.openmeteo import build_snapshot_rows

Base.metadata.create_all(bind=engine)

async def main():
    db = SessionLocal()
    try:
        crud.init_models(db)
        locations = crud.list_locations(db)
        enabled_models = [m.name for m in crud.list_models(db) if m.enabled]

        for loc in locations:
            print(f"Processing {loc.name}")
            for model_name in enabled_models:
                try:
                    rows = await build_snapshot_rows(loc.latitude, loc.longitude, loc.timezone, model_name)
                    count = 0
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
                        count += 1
                    print(f"  {model_name}: {count}")
                except Exception as e:
                    print(f"  skipped {model_name}: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main())
