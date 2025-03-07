from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean
from .base import Base
from datetime import datetime

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    capacity = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)