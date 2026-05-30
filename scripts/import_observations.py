import csv
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "backend"))

from app.db import SessionLocal, Base, engine
from app import crud, models

Base.metadata.create_all(bind=engine)

def parse_dt(value: str):
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt

def main(csv_path: str):
    db = SessionLocal()
    try:
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                obs = models.Observation(
                    location_id=int(row["location_id"]),
                    observed_time=parse_dt(row["observed_time"]),
                    temperature_2m=float(row["temperature_2m"]) if row.get("temperature_2m") else None,
                    wind_speed_10m=float(row["wind_speed_10m"]) if row.get("wind_speed_10m") else None,
                    precipitation=float(row["precipitation"]) if row.get("precipitation") else None,
                    raw_json=json.dumps(row),
                )
                crud.add_observation(db, obs)
                print(f"saved observation location={obs.location_id} time={obs.observed_time}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/import_observations.py observations.csv")
        raise SystemExit(1)
    main(sys.argv[1])
