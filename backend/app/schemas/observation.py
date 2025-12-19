from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ObservationBase(BaseModel):
    species: str
    date: datetime
    latitude: float
    longitude: float
    notes: Optional[str] = None
    category: str

class ObservationCreate(ObservationBase):
    pass

class ObservationUpdate(BaseModel):
    species: Optional[str] = None
    date: Optional[datetime] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    notes: Optional[str] = None
    category: Optional[str] = None

class Observation(ObservationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
