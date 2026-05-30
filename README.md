# Weather Tracker

A self-hosted, free weather comparison app for multiple locations and multiple forecast models.

## Features
- Save many locations
- Compare models per location
- Store forecast snapshots on a schedule
- Compare by lead time: 7d, 4d, 48h, 24h, 12h, 6h, 3h, 2h, 1h, 30m
- TrueNAS Scale friendly Docker deployment

## Notes
Open-Meteo provides free access, no API key, 30+ models, a 7-day hourly forecast API, historical forecast archives, and previous-run analysis support. [web:20][web:14][web:18]

## Run
1. Copy `.env.example` to `.env`
2. Replace `YOUR_TRUENAS_IP` in `.env`
3. Run:

```bash
docker compose up --build
```

4. Open:
- Frontend: `http://YOUR_TRUENAS_IP:7101`
- Backend: `http://YOUR_TRUENAS_IP:8000/docs`

## Workflow
1. Add locations.
2. Let snapshots run.
3. Wait a few days.
4. Compare model performance by lead time.
