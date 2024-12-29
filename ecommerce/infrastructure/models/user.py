import ulid
from sqlalchemy import Column, Integer, String, Text

from ecommerce.infrastructure.database.sql import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ulid()))
    name = Column(String(255), nullable=False)
    document = Column(String(11))
    username = Column(String(50))
    password = Column(Text)
    email = Column(String(255))
    phone = Column(String(20))
    balance = Column(Integer)
    avatar = Column(Text)
    refer = Column(String(26))


