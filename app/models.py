from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


# ✅ Product Table (Stores product details)
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    manufacturer = Column(String, nullable=False)

    # Relationship: One product can have multiple stock entries
    stock = relationship("Stock", back_populates="product")


# ✅ Stock Table (Stores stock quantity for products)
class Stock(Base):
    __tablename__ = "stock"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    # Relationship: Links stock entry to the corresponding product
    product = relationship("Product", back_populates="stock")
