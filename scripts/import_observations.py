import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from app.db import SessionLocal, Base, engine
from app import crud, models
from app.openmeteo import build_observation_rows

Base.metadata.create_all(bind=engine)

async def main(days_back: int = 14):
    db = SessionLocal()
    try:
        crud.init_models(db)
        end = datetime.now(timezone.utc).date()
        start = end - timedelta(days=days_back)

        for loc in crud.list_locations(db):
            try:
                rows = await build_observation_rows(loc.latitude, loc.longitude, loc.timezone, start.isoformat(), end.isoformat())
                count = 0
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
                    count += 1
                print(f"{loc.name}: {count}")
            except Exception as e:
                print(f"skipped {loc.name}: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    days_back = int(sys.argv[1]) if len(sys.argv) > 1 else 14
    asyncio.run(main(days_back))
