from sqlalchemy.orm import Session
from sqlalchemy import and_
from geopy.geocoders import Nominatim
from fastapi import HTTPException
from datetime import datetime
from app.models.events import Events
from app.schemas.event import EventCreate, EventResponse




def get_coordinates_from_city(city_name: str):
    #Şehir ismini GPS koordinatlarına çevirir
    geolocator = Nominatim(user_agent="bmt_event_app_v1")
    try:
        # Türkiye aramaları için sonuna ekleme yapıyoruz
        location = geolocator.geocode(f"{city_name}, Turkey")
        if location:
            return location.latitude, location.longitude
    except Exception:
        return None, None
    return None, None
def create_event(db: Session, event_in: EventCreate):

    #Yeni bir etkinlik oluşturur
    #Kullanıcının girdiği şehir ismini otomatik koordinata çevirir
    lat, lon = get_coordinates_from_city(event_in.city_name)
    if lat is None:
        raise HTTPException(status_code=400,detail="Girdiğiniz şehir ismi doğrulanamadı. Lütfen geçerli bir şehir yazın.")

    db_event = Events(
        event_name=event_in.event_name,
        description=event_in.description,
        creator_id=event_in.creator_id,
        image_url=event_in.image_url,
        event_date=event_in.event_date,
        event_time=event_in.event_time,
        quota=event_in.quota,
        seating_arrangement_url=event_in.seating_arrangement_url,
        city_name=event_in.city_name,
        latitude=lat,
        longitude=lon,
        created_at=datetime.utcnow()
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_event_by_id(db: Session, event_id: int):
    """ID'ye göre tek bir etkinlik getirir."""
    return db.query(Events).filter(Events.event_id == event_id).first()


def get_all_events(db: Session, skip: int = 0, limit: int = 100):
    """Tüm etkinlikleri listeler."""
    return db.query(Events).offset(skip).limit(limit).all()


def search_events_by_location(
        db: Session,
        lat: float = None,
        lon: float = None,
        city_name: str = None,
        radius_km: float = 50.0
):
    """
    KONUM TABANLI FİLTRELEME:
    1. GPS (lat/lon) varsa direkt mesafe hesabı yapar.
    2. Sadece Şehir ismi varsa, o şehrin merkezine göre hesap yapar.
    3. Hiçbiri yoksa tüm etkinlikleri döner.
    """
    target_lat, target_lon = lat, lon

    # Koordinat yoksa ama şehir ismi girildiyse şehri koordinata çevir
    if target_lat is None and city_name:
        target_lat, target_lon = get_coordinates_from_city(city_name)

    # Eğer hala koordinat yoksa (parametre gönderilmemişse) tümünü getir
    if target_lat is None:
        return db.query(Events).all()

    # SQLite Bounding Box (Sınırlayıcı Kutu) Filtresi:
    # Dünya üzerinde 1 derece enlem yaklaşık 111 km'dir.
    margin = radius_km / 111.0

    return db.query(Events).filter(
        and_(
            Events.latitude.between(target_lat - margin, target_lat + margin),
            Events.longitude.between(target_lon - margin, target_lon + margin)
        )
    ).all()


def delete_event(db: Session, event_id: int):
    """Etkinliği siler."""
    db_event = db.query(Events).filter(Events.event_id == event_id).first()
    if db_event:
        db.delete(db_event)
        db.commit()
    return db_event