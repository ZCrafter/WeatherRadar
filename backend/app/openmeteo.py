import httpx

OPENMETEO_BASE = "https://api.open-meteo.com/v1/forecast"

async def fetch_forecast(latitude: float, longitude: float, timezone: str = "auto"):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m,wind_speed_10m,precipitation",
        "forecast_days": 7,
        "timezone": timezone,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.get(OPENMETEO_BASE, params=params)
        r.raise_for_status()
        return r.json()
