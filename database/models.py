from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    picture = Column(String, nullable=True)
    
    image_quota = Column(Integer, default=15)
    video_quota = Column(Integer, default=5)
    
    created_at = Column(DateTime, default=datetime.utcnow)