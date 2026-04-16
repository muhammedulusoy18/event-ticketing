from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_password_hash


# Kullanıcıyı E-posta Adresinden Bulma
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# Yeni Kullanıcı Oluşturma (Kayıt)
def create_user_default(db: Session, user: UserCreate):
    # Şifreyi açık haliyle değil, hashleyerek alıyoruz
        hashed_password = get_password_hash(user.password)
        db_user = User(
        email=user.email,
        hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user
def create_user_admin(db: Session, user: UserCreate):
    # Veritabanı modelini oluşturuyoruz
    db_user = User(
        email=user.email,
        hashed_password= get_password_hash(user.password),
        role=user.role
    )

    # Veritabanına ekle ve kaydet
    db.add(db_user)
    db.commit()

    # Veritabanındaki son halini  nesneye geri yükle
    db.refresh(db_user)

    return db_user
def check_mail(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
def change_password(db: Session, user: User, new_password: str):
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.commit()
    db.refresh(user)
    return user