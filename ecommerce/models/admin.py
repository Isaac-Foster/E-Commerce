
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from ecommerce.database.sql import Base


class AdminModel(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(26), ForeignKey("users.id"), nullable=False)
    password = Column(Text)
