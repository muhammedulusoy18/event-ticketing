import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.models.user import User
from app.models.events import Events
from app.db.database import engine, Base as AuthBase
from app.db.eventsDb import engine as eventEngine, Base as EventBase

from app.api import auth, events

# klasör kontrolü
if not os.path.exists("static/event_images"):
    os.makedirs("static/event_images", exist_ok=True)

#tabloları oluşturma
AuthBase.metadata.create_all(bind=engine)
EventBase.metadata.create_all(bind=eventEngine)

app = FastAPI(title="BMT Event & Auth Service")

# statik dosyaları dışarıya açma
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(events.router)

@app.get("/")
def read_root():
    return {
        "message": "Etkinlik ve Kimlik Doğrulama Servisi Aktif!"
    }