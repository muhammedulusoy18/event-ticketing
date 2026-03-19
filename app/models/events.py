from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime,Float
from app.db.eventsDb import Base
from app.models.user import User
class Events(Base):
    __tablename__ = "events"
    event_id=Column(Integer, primary_key=True,index=True)
    event_name=Column(String,index=True)
    creator_id=Column(Integer,index=True)
    image_url=Column(String,index=True)
    description=Column(String,index=True)
    event_date=Column(DateTime,index=True)
    event_time=Column(DateTime,index=True)
    created_at=Column(DateTime,index=True,default=datetime.utcnow)
    quota=Column(Integer,index=True,default=0,nullable=False)
    seating_arrangement_url=Column(String,index=True)
    latitude=Column(Float,nullable=False)
    longitude= Column(Float,nullable=False)
    city_name=Column(String,nullable=False)


