from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from ..database import get_db
from ..models import Location as LocationModel, Observation as ObservationModel
from ..schemas import Location, LocationCreate, LocationUpdate, LocationWithCount, PaginatedResponse

router = APIRouter(prefix="/locations", tags=["locations"])

@router.get("", response_model=PaginatedResponse[LocationWithCount])
def get_locations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    total = db.query(LocationModel).count()

    # Query locations with observation count
    locations_query = db.query(
        LocationModel,
        func.count(ObservationModel.id).label('observation_count')
    ).outerjoin(ObservationModel).group_by(LocationModel.id).order_by(LocationModel.id.desc()).offset(skip).limit(limit).all()

    # Transform to LocationWithCount
    locations = []
    for location, count in locations_query:
        location_dict = {
            "id": location.id,
            "name": location.name,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "description": location.description,
            "address": location.address,
            "created_at": location.created_at,
            "updated_at": location.updated_at,
            "observation_count": count
        }
        locations.append(location_dict)

    return {"data": locations, "total": total}

@router.get("/{location_id}", response_model=LocationWithCount)
def get_location(location_id: int, db: Session = Depends(get_db)):
    location = db.query(LocationModel).filter(LocationModel.id == location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    # Get observation count
    observation_count = db.query(func.count(ObservationModel.id)).filter(ObservationModel.location_id == location_id).scalar()

    return {
        "id": location.id,
        "name": location.name,
        "latitude": location.latitude,
        "longitude": location.longitude,
        "description": location.description,
        "address": location.address,
        "created_at": location.created_at,
        "updated_at": location.updated_at,
        "observation_count": observation_count
    }

@router.post("", response_model=Location, status_code=201)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    db_location = LocationModel(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

@router.put("/{location_id}", response_model=Location)
def update_location(location_id: int, location: LocationUpdate, db: Session = Depends(get_db)):
    db_location = db.query(LocationModel).filter(LocationModel.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")

    update_data = location.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_location, key, value)

    db.commit()
    db.refresh(db_location)
    return db_location

@router.delete("/{location_id}", status_code=204)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(LocationModel).filter(LocationModel.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")

    db.delete(db_location)
    db.commit()
    return None
