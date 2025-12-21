from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LocationBase(BaseModel):
    name: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    address: Optional[str] = None


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    description: Optional[str] = None
    address: Optional[str] = None


class Location(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LocationWithCount(Location):
    observation_count: int
