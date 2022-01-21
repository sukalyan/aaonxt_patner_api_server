from sqlalchemy import Column, Integer, String
from app.database import Base


class UserInfo(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    name = Column(String, index=True)
    organization = Column(String, index=True)
    password = Column(String)
    created_on = Column(String)
    email_varification_code = Column(String)
    public_id = Column(String)
    is_active = Column(Integer)
    