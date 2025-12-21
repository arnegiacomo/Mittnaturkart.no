from pydantic import BaseModel, field_validator
from datetime import datetime, timezone
from typing import Optional, List, Generic, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from .location import Location

class ObservationBase(BaseModel):
    species: str
    date: datetime
    location_id: Optional[int] = None
    notes: Optional[str] = None
    category: str

    @field_validator('date', mode='before')
    @classmethod
    def ensure_timezone_aware(cls, v):
        if isinstance(v, str):
            return v  # Pydantic handles ISO 8601 parsing
        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)  # Assume UTC if naive
        return v

class ObservationCreate(ObservationBase):
    pass

class ObservationUpdate(BaseModel):
    species: Optional[str] = None
    date: Optional[datetime] = None
    location_id: Optional[int] = None
    notes: Optional[str] = None
    category: Optional[str] = None

class Observation(ObservationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    location: Optional['Location'] = None

    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def ensure_timestamps_timezone_aware(cls, v):
        if isinstance(v, str):
            return v  # Pydantic handles ISO 8601 parsing
        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)  # Assume UTC if naive
        return v

    class Config:
        from_attributes = True

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]
    total: int

# Resolve forward references after Location is imported
def _resolve_forward_refs():
    from .location import Location as LocationSchema
    Observation.model_rebuild(_types_namespace={'Location': LocationSchema})

_resolve_forward_refs()
