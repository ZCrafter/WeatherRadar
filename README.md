# Weather Tracker

Self-hosted, free weather forecast comparison app for multiple locations and models.

## Features
- Multiple locations
- Multiple free weather models (Open-Meteo, 30+ models)
- Automatic forecast snapshot collection
- Lead-time comparison: 7d, 4d, 48h, 24h, 12h, 6h, 3h, 2h, 1h, 30m
- TrueNAS Scale friendly

## Run
1. Copy `.env.example` to `.env`
2. Replace `YOUR_TRUENAS_IP` with your TrueNAS IP address
3. Run:

```bash
docker compose up --build -d
```

4. Open:
   - Frontend: `http://YOUR_TRUENAS_IP:7101`
   - Backend docs: `http://YOUR_TRUENAS_IP:8000/docs`

## Workflow
1. Add locations in the UI
2. Snapshots are collected automatically every 30 minutes
3. After a few days, compare model performance
