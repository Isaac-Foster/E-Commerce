from datetime import datetime

from sqlalchemy import Column, String, Integer, func, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from database.sql import Base, engine


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=func.uuid_generate_v4())
    name = Column(String(255), nullable=False)
    document = Column(String(11))
    username = Column(String(50))
    password = Column(Text)
    email = Column(String(255))
    phone = Column(String(20))
    balance = Column(Integer)
    avatar = Column(Text)
    refer = Column(String(36))
    
    
