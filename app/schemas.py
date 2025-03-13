from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, example="Laptop")
    price: float = Field(..., gt=0, example=999.99)
    category: str = Field(..., min_length=3, max_length=50, example="Electronics")
    manufacturer: str = Field(..., min_length=2, max_length=50, example="Dell")


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=3, max_length=50)
    manufacturer: Optional[str] = Field(None, min_length=2, max_length=50)


class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str
    manufacturer: str

    class Config:
        from_attributes = True  # ✅ Allows converting SQLAlchemy model to Pydantic schema


class StockCreate(BaseModel):
    product_id: int = Field(..., example=1)
    quantity: int = Field(..., ge=0, example=50)


class StockUpdate(BaseModel):
    quantity: int = Field(..., ge=0, example=100)


class Stock(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True
