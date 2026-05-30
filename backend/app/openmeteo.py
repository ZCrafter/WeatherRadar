import httpx
from datetime import datetime, timezone

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/archive"

async def fetch_forecast(latitude: float, longitude: float, timezone_name: str = "auto", model: str | None = None):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,wind_speed_10m,precipitation",
        "forecast_days": 7,
        "timezone": timezone_name,
    }
    if model:
        params["models"] = model
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(FORECAST_URL, params=params)
        if r.status_code >= 400:
            raise RuntimeError(f"Open-Meteo error {r.status_code}: {r.text[:300]}")
        r.raise_for_status()
        return r.json()

async def fetch_historical(latitude: float, longitude: float, start_date: str, end_date: str, timezone_name: str = "auto"):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,wind_speed_10m,precipitation",
        "start_date": start_date,
        "end_date": end_date,
        "timezone": timezone_name,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(HISTORICAL_URL, params=params)
        r.raise_for_status()
        return r.json()

def lead_bucket(minutes: int) -> int:
    choices = [30, 60, 120, 180, 360, 720, 1440, 2880, 5760, 8640]
    return min(choices, key=lambda x: abs(x - minutes))

async def build_snapshot_rows(latitude: float, longitude: float, timezone_name: str, model: str):
    data = await fetch_forecast(latitude, longitude, timezone_name, model=model)
    now = datetime.now(timezone.utc)
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    winds = hourly.get("wind_speed_10m", [])
    precs = hourly.get("precipitation", [])

    out = []
    for i, t in enumerate(times):
        target = datetime.fromisoformat(t)
        if target.tzinfo is None:
            target = target.replace(tzinfo=timezone.utc)
        lead = int((target - now).total_seconds() / 60)
        if lead < 0:
            continue
        out.append({
            "run_time": now,
            "target_time": target,
            "lead_minutes": lead,
            "bucket_minutes": lead_bucket(lead),
            "temperature_2m": temps[i] if i < len(temps) else None,
            "wind_speed_10m": winds[i] if i < len(winds) else None,
            "precipitation": precs[i] if i < len(precs) else None,
            "raw_json": data,
        })
    return out

async def build_observation_rows(latitude: float, longitude: float, timezone_name: str, start_date: str, end_date: str):
    data = await fetch_historical(latitude, longitude, start_date, end_date, timezone_name)
    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    winds = hourly.get("wind_speed_10m", [])
    precs = hourly.get("precipitation", [])

    out = []
    for i, t in enumerate(times):
        dt = datetime.fromisoformat(t)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        out.append({
            "observed_time": dt,
            "temperature_2m": temps[i] if i < len(temps) else None,
            "wind_speed_10m": winds[i] if i < len(winds) else None,
            "precipitation": precs[i] if i < len(precs) else None,
            "raw_json": data,
        })
    return out
