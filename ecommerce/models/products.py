from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from ecommerce.database.sql import Base


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    image = Column(Text)
    price = Column(Integer)

    # Relacionamento one-to-many, com delete-orphan no lado "one"
    variations = relationship("ProductVariationModel", back_populates="product", cascade="all, delete-orphan")
    images = relationship("ProductImageModel", back_populates="product", cascade="all, delete-orphan")
    videos = relationship("ProductVideoModel", back_populates="product", cascade="all, delete-orphan")


class ProductVariationModel(Base):
    __tablename__ = "product_variations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    color = Column(String(100), nullable=True) 
    size = Column(String(100), nullable=True) 
    price = Column(Integer, nullable=True)
    quantity = Column(Integer, nullable=False)

    product = relationship("ProductModel", back_populates="variations")


class ProductImageModel(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    image_url = Column(Text, nullable=False)

    product = relationship("ProductModel", back_populates="images")


class ProductVideoModel(Base):
    __tablename__ = "product_videos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    video_url = Column(Text, nullable=False)

    product = relationship("ProductModel", back_populates="videos")
