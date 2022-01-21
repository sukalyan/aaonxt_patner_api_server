from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from . import models, schemas
from datetime import datetime
import uuid
from random import randint


def alluser(db: Session):
    return db.query(models.UserInfo).all()
    
def get_user_by_username(db: Session, email: str):
    return db.query(models.UserInfo).filter(models.UserInfo.email == email).first()

def get_user_by_public_id(db: Session, public_id: str):
    return db.query(models.UserInfo).filter(models.UserInfo.public_id == public_id).first()

def check_username_password(db: Session, user: schemas.UserAuthenticate):
    db_user_info: models.UserInfo = get_user_by_username(db, email=user.email)
    return check_password_hash(db_user_info.password,user.password)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = generate_password_hash(user.password, method='sha256')
    public_id=str(uuid.uuid4())
    VARIFICATION_CODE = randint(100000, 999999)
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d")
    db_user = models.UserInfo(email=user.email,name=user.name,organization=user.organization, password=hashed_password,public_id=public_id,email_varification_code=VARIFICATION_CODE,created_on=str(dt_string),is_active=1)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
