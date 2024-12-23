import ulid
from sqlalchemy import Column, Integer, String, Text

from ecommerce.database.sql import Base


class RestricPathModel(Base):
    __tablename__ = "restric_paths"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(512), nullable=False)
    origin = Column(String(12), nullable=False)