from sqlalchemy import Column, Integer, String, Text, DECIMAL, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    base_price = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    description = Column(Text)
    image_url = Column(String(255))
    category = Column(String(100), nullable=False, index=True)

    # Зв'язок з таблицею розмірів
    sizes = relationship("Size", back_populates="product", cascade="all, delete-orphan")

class Size(Base):
    __tablename__ = "sizes"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False, index=True)
    size_name = Column(String(255), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)

    # Зв'язок назад до продукту
    product = relationship("Product", back_populates="sizes")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(255), nullable=False)
    client_phone = Column(String(50), nullable=False)
    order_date = Column(DateTime, default=func.now(), nullable=False)
    product_name = Column(String(255), nullable=False)
    product_size = Column(String(255))
    quantity = Column(Integer, nullable=False)
    total_price = Column(DECIMAL(10, 2), nullable=False)