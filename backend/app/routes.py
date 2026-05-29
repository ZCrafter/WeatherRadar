from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db, Base, engine
from app import crud, schemas, models
from app.openmeteo import fetch_forecast

router = APIRouter(prefix="/api")

Base.metadata.create_all(bind=engine)

@router.get("/locations", response_model=list[schemas.LocationRead])
def read_locations(db: Session = Depends(get_db)):
    return crud.list_locations(db)

@router.post("/locations", response_model=schemas.LocationRead)
def add_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    return crud.create_location(db, location)

@router.delete("/locations/{location_id}")
def remove_location(location_id: int, db: Session = Depends(get_db)):
    obj = crud.delete_location(db, location_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"deleted": location_id}

@router.get("/forecast/{location_id}")
async def forecast_for_location(location_id: int, db: Session = Depends(get_db)):
    loc = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")
    data = await fetch_forecast(loc.latitude, loc.longitude, loc.timezone)
    return {"location": loc.name, "forecast": data}
