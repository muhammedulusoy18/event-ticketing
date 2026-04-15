import uuid
from app.db.eventsDb import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean


class Tickets(Base):

    __tablename__ = "tickets"
    ticket_id=Column(Integer,primary_key=True)
    event_id=Column(Integer, ForeignKey("events.event_id"),nullable=False)
    user_id=Column( Integer,nullable=False)
    purchase_date=Column(DateTime,nullable=False)
    quantity=Column(Integer,nullable=False)
    ticket_uuid = Column(String, default=lambda: str(uuid.uuid4()), unique=True)
    is_used=Column(Boolean,default=False)