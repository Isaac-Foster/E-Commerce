from sqlalchemy import Column, ForeignKey, Integer, String, Text, JSON
from ecommerce.infrastructure.database.sql import Base


class AdminModel(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(26), ForeignKey("users.id"), nullable=False)
    password = Column(Text)
    privileges = Column(JSON, nullable=True)
