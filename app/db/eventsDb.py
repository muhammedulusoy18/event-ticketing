from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from app.core.config import settings

engine =create_engine(settings.EVENTDB_URL, connect_args={"check_same_thread": False}
                     )
SessionLocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)
Base=declarative_base()

def get_Eventdb():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()