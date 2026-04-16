from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.api.auth import get_current_user

from app.schemas.tickets import TicketPurchaseCreate, TicketResponse
from app.crud.tickets import create_ticket_purchase
from app.models.user import User
from app.db.eventsDb import get_Eventdb
from app.models.tickets import Tickets
from app.core.security import check_role
router = APIRouter(
    prefix="/tickets",
    tags=["Bilet İşlemleri"]
)



@router.post("/buy/{event_id}")
def buy_ticket(
    event_id: int,
    ticket_data: TicketPurchaseCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_Eventdb),
    current_user: User = Depends(get_current_user) ):
    user_id= current_user.id

    purchased_ticket = create_ticket_purchase(
        db=db,
        event_id=event_id,
        user_id=user_id,
        ticket_data=ticket_data,
        background_tasks=background_tasks
    )

    return purchased_ticket
@router.post("/validate")
def validate_ticket(
        ticket_uuid: str,
        db: Session = Depends(get_Eventdb),
        current_user: User = Depends(get_current_user)
        ):
        if check_role(current_user) < 1:
            raise HTTPException(status_code=403,detail="Bu işlem için yetkiniz yok. Sadece görevliler bilet doğrulayabilir.")
        ticket=db.query(Tickets).filter(Tickets.ticket_uuid == ticket_uuid).first()
        if not ticket:
            raise HTTPException(status_code=404,detail="Bilet bulunamadı.")
        if ticket.is_used:
            raise HTTPException(status_code=400,detail=f"Bu bilet daha önce kullanılmış!")
        ticket.is_used = True
        db.commit()
        return {"status": "success",
                "message": "Bilet onaylandı! Giriş serbest.",
                "ticket_details": {
                "event_name": ticket.event.event_name,
                "quantity": ticket.quantity,
                "owner_id": ticket.user_id}}
@router.get("/my",response_model=List[TicketResponse])
def get_my_tickets(db: Session = Depends(get_Eventdb), current_user: User = Depends(get_current_user)):
    my_tickets=db.query(Tickets).filter(Tickets.user_id == current_user.id).all()
    if not my_tickets:
        return []
    return my_tickets
@router.delete("/{ticket_uuid}/delete")
def delete_ticket(ticket_uuid:str,current_user: User = Depends(get_current_user),db: Session = Depends(get_Eventdb)):
    ticket = db.query(Tickets).filter(Tickets.ticket_uuid == ticket_uuid).first()
    if ticket is None:
        raise HTTPException(status_code=404,detail="Böyle bir bilet bulunamadı.")

    if ticket.is_used:
        raise HTTPException(status_code=400, detail="Bu bilet kullanıldığı için ipta edilemez")
    if ticket.user_id != current_user.id:
        raise HTTPException(status_code=403,detail="böyle bir biletiniz yok.")
    ticket.event.quota+=ticket.quantity
    db.delete(ticket)
    db.commit()
    return {"message": "Bilet başarıyla silindi kota iade edildi"}

