from datetime import datetime

from pydantic import BaseModel,Field
from sqlalchemy import Boolean


class TicketPurchaseCreate(BaseModel):
    quantity: int=Field(...,gt=0,description="Satın alınmak istenen bilet adedi")
class TicketResponse(BaseModel):
    ticket_id: int
    event_id: int
    quantity: int
    is_ude: bool
    purchase_date: datetime
    class config:
        orm_mode = True
