from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models import Observation as ObservationModel
from ..schemas import Observation, ObservationCreate, ObservationUpdate, PaginatedResponse

router = APIRouter(prefix="/observations", tags=["observations"])

@router.get("", response_model=PaginatedResponse[Observation])
def get_observations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    total = db.query(ObservationModel).count()
    observations = db.query(ObservationModel).order_by(ObservationModel.id.desc()).offset(skip).limit(limit).all()
    return {"data": observations, "total": total}

@router.get("/{observation_id}", response_model=Observation)
def get_observation(observation_id: int, db: Session = Depends(get_db)):
    observation = db.query(ObservationModel).filter(ObservationModel.id == observation_id).first()
    if not observation:
        raise HTTPException(status_code=404, detail="Observation not found")
    return observation

@router.post("", response_model=Observation, status_code=201)
def create_observation(observation: ObservationCreate, db: Session = Depends(get_db)):
    db_observation = ObservationModel(**observation.model_dump())
    db.add(db_observation)
    db.commit()
    db.refresh(db_observation)
    return db_observation

@router.put("/{observation_id}", response_model=Observation)
def update_observation(observation_id: int, observation: ObservationUpdate, db: Session = Depends(get_db)):
    db_observation = db.query(ObservationModel).filter(ObservationModel.id == observation_id).first()
    if not db_observation:
        raise HTTPException(status_code=404, detail="Observation not found")

    update_data = observation.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_observation, key, value)

    db.commit()
    db.refresh(db_observation)
    return db_observation

@router.delete("/{observation_id}", status_code=204)
def delete_observation(observation_id: int, db: Session = Depends(get_db)):
    db_observation = db.query(ObservationModel).filter(ObservationModel.id == observation_id).first()
    if not db_observation:
        raise HTTPException(status_code=404, detail="Observation not found")

    db.delete(db_observation)
    db.commit()
    return None
