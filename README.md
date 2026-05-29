# Weather Tracker

Free local weather tracker for comparing forecast models across multiple locations and lead times.

## What it does
- Save several locations
- Pull free Open-Meteo forecasts
- Prepare for model comparison over time
- TrueNAS Scale friendly Docker setup

## Lead times
Designed for:
- 7 days
- 4 days
- 48 hours
- 24 hours
- 12 hours
- 6 hours
- 3 hours
- 2 hours
- 1 hour
- 30 minutes

Open-Meteo Previous Runs API supports 1–7 day offsets directly, and you can store shorter lead-time snapshots locally by polling on a schedule. [web:14][web:20]

## Run locally
1. Copy `.env.example` to `.env`
2. Run `docker compose up --build`
3. Open:
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000/docs

## Notes
- Open-Meteo has no API key requirement and supports 30+ weather models. [web:1]
- Multiple coordinates are supported by Open-Meteo APIs. [web:20][web:23]
