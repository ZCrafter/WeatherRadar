from sqlalchemy.orm import Session
from app import models, schemas

def list_locations(db: Session):
    return db.query(models.Location).order_by(models.Location.name.asc()).all()

def create_location(db: Session, location: schemas.LocationCreate):
    obj = models.Location(**location.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def delete_location(db: Session, location_id: int):
    obj = db.query(models.Location).filter(models.Location.id == location_id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj
