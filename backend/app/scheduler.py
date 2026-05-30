import json
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from app.config import settings
from app.db import SessionLocal
from app import crud, models
from app.openmeteo import build_snapshot_rows

scheduler = BackgroundScheduler()

async def collect_all_snapshots():
    db = SessionLocal()
    try:
        crud.init_models(db)
        locations = crud.list_locations(db)
        enabled_models = [m.name for m in crud.list_models(db) if m.enabled]

        for loc in locations:
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
                except Exception:
                    continue
    finally:
        db.close()

def run_collection():
    asyncio.run(collect_all_snapshots())

def start_scheduler():
    scheduler.add_job(run_collection, "interval", minutes=settings.scheduler_interval_minutes, id="snapshot_job", replace_existing=True)
    scheduler.start()

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown(wait=False)
