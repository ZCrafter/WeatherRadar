# Weather Tracker

Free local weather tracker for comparing many weather models across many locations and lead times.

## Features
- Multiple saved locations
- Open-Meteo model comparison
- Scheduled forecast snapshots
- Lead-time buckets from 7d down to 30m
- Forecast error scoring
- TrueNAS Scale friendly Docker deployment

## How it works
Open-Meteo provides free access with no API key, 30+ weather models, 7-day hourly forecast data, and Previous Runs support for 1–7 day offsets. [web:1][web:20][web:14]
For shorter lead times like 12h, 6h, 3h, 2h, 1h, and 30m, the app stores its own snapshots locally.

## Run
1. Copy `.env.example` to `.env`
2. Run `docker compose up --build`
3. Open `http://localhost:3000`

## API
- `GET /api/locations`
- `POST /api/locations`
- `DELETE /api/locations/{id}`
- `GET /api/models`
- `POST /api/snapshot/{location_id}`
- `GET /api/comparison/{location_id}`
