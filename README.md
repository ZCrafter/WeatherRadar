# Weather Radar

Self-hosted weather model comparison app.

## What it does
- Stores many locations
- Stores forecasts by model, lead time, and target timestamp
- Stores historical observations
- Compares temperature and precipitation forecast skill
- Shows score tables and time-series error charts per location

## Why scores are different now
Scores are computed separately by:
- location
- model
- lead time bucket
- metric
- timestamp

This lets you see whether a model is good at 7 days out but weak at 1 hour out.

## Run
1. Copy `.env.example` to `.env`
2. Set `YOUR_TRUENAS_IP`
3. Run:

```bash
docker compose up --build -d
```

4. Backfill once:

```bash
docker compose exec backend python /scripts/backfill.py
docker compose exec backend python /scripts/import_observations.py 14
```

## Notes
Open-Meteo offers 30+ models and multiple forecast/historical endpoints. [web:20][web:1][web:18][web:114]
