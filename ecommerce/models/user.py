
from sqlalchemy import Column, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID

from ecommerce.database.sql import Base


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


