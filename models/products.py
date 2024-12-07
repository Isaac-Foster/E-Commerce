from sqlalchemy import Column, String, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from database.sql import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False) 
    description = Column(Text)
    image = Column(Text)
    price = Column(Integer)
    variations = relationship("ProductVariationModel", back_populates="product")


class ProductVariationModel(Base):
    __tablename__ = "product_variations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False) 
    color = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False) 
    price = Column(Integer)
    product = relationship("ProductModel", back_populates="variations")
