from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from datetime import datetime, timezone
from uuid import UUID


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
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def ensure_timezone_aware(cls, v):
        if isinstance(v, str):
            return v  # Pydantic handles ISO 8601 parsing
        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)  # Assume UTC if naive
        return v

    model_config = ConfigDict(from_attributes=True)


class LocationWithCount(Location):
    observation_count: int
