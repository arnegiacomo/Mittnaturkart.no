from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from datetime import datetime
from ..database import Base

class Observation(Base):
    __tablename__ = "observations"

    id = Column(Integer, primary_key=True, index=True)
    species = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)
    category = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
