from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

#ortak alanları içeren ana şema
class EventBase(BaseModel):
    event_name: str
    description: Optional[str] = None
    event_date: datetime
    event_time: datetime
    quota: int = 0
    image_url: Optional[str] = None
    seating_arrangement_url: Optional[str] = None

#etkinlik oluştururken kullanıcıdan beklediğimiz şema
class EventCreate(EventBase):
    city_name: str  # Kullanıcı koordinat değil, şehir ismi girecek
    creator_id: int

#veritabanından veri dönerken kullanacağımız şema
class EventResponse(EventBase):
    event_id: int
    creator_id: int
    created_at: datetime
    latitude: float
    longitude: float
    city_name: str
    model_config = ConfigDict(from_attributes=True)

#filtreleme için basit bir konum şeması
class NearbySearch(BaseModel):
    user_lat: float
    user_lon: float
    radius_km: float = 10.0