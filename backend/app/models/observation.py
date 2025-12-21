from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True, index=True)
    species = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id", ondelete="SET NULL"), nullable=True)
    notes = Column(Text, nullable=True)
    category = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    location = relationship("Location", back_populates="observations")
