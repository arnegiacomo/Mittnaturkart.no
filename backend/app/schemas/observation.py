from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Generic, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from .location import Location

class ObservationBase(BaseModel):
    species: str
    date: datetime
    location_id: Optional[int] = None
    notes: Optional[str] = None
    category: str

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
