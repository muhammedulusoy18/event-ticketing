import os
import shutil
from uuid import uuid4
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.db.eventsDb import get_Eventdb
from app.api.auth import get_current_user
from app.schemas.user import UserResponse
from app.schemas.event import EventCreate, EventResponse
from app.crud import event as crud_event
from app.core import security

router = APIRouter(prefix="/events", tags=["sharing events"])

#görsellerin kaydedileceği klasör
UPLOAD_DIR = "static/event_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/shareEvent", response_model=EventResponse)
async def share_event(
    event_name: str = Form(...),
    description: Optional[str] = Form(None),
    event_date: str = Form(...),
    event_time: str = Form(...),
    city_name: str = Form(...),
    quota: int = Form(0),
    image: UploadFile = File(...), # Kullanıcıdan gelen dosya
    current_user: UserResponse = Depends(get_current_user),
    db: Session = Depends(get_Eventdb)
):
    print(f"DEBUG - Mevcut Kullanıcı Rolü: '{current_user.role}'")
    user_score = security.check_role({"role": current_user.role})
    print(f"DEBUG - Hesaplanan Yetki Skoru: {user_score}")
    #yetki kontrolü
    user_score = security.check_role({"role": current_user.role})
    if user_score < 1:
        raise HTTPException(status_code=403, detail="Etkinlik paylaşma yetkiniz yok.")

    # resmi sunucuya kaydetme
    file_extension = image.filename.split(".")[-1]
    unique_filename = f"{uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    #veritabanına yazılacak resim yolu
    image_url = f"/static/event_images/{unique_filename}"

    #tarih ve saat dönüşümü
    try:
        date_obj = datetime.strptime(event_date, "%Y-%m-%d")
        time_obj = datetime.strptime(event_time, "%H:%M")
    except ValueError:
        raise HTTPException(status_code=400, detail="Tarih(YYYY-MM-DD) veya Saat(HH:MM) formatı yanlış.")

    # şemayı oluştur ve CRUD'a Gönder
    event_in = EventCreate(
        event_name=event_name,
        description=description,
        event_date=date_obj,
        event_time=time_obj,
        city_name=city_name,
        quota=quota,
        creator_id=current_user.id,
        image_url=image_url
    )

    return crud_event.create_event(db=db, event_in=event_in)

@router.get("/nearby", response_model=List[EventResponse])
def get_nearby_events(
    city: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius: float = 50.0,
    db: Session = Depends(get_Eventdb)
):

    #Kullanıcı ya şehir ismi girer ya da GPS gönderir.
    #radius: Arama yarıçapı

    return crud_event.search_events_by_location(
        db=db, lat=lat, lon=lon, city_name=city, radius_km=radius
    )

@router.get("/all", response_model=List[EventResponse])
def read_all_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_Eventdb)):
    #tüm etkinlikleri listeler
    return crud_event.get_all_events(db, skip=skip, limit=limit)