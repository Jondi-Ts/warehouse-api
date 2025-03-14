from pydantic import BaseModel, Field
from typing import Optional


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, example="Laptop",
                      description="Product name (3-100 characters)")
    price: float = Field(..., gt=0, example=999.99, description="Price must be a positive number")
    category: str = Field(..., min_length=3, max_length=50, example="Electronics",
                          description="Category (3-50 characters)")
    manufacturer: str = Field(..., min_length=2, max_length=50, example="Dell",
                              description="Manufacturer (2-50 characters)")


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100, description="Updated product name")
    price: Optional[float] = Field(None, gt=0, description="Updated product price (must be positive)")
    category: Optional[str] = Field(None, min_length=3, max_length=50, description="Updated category name")
    manufacturer: Optional[str] = Field(None, min_length=2, max_length=50, description="Updated manufacturer name")


class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str
    manufacturer: str

    class Config:
        from_attributes = True


class StockCreate(BaseModel):
    product_id: int = Field(..., gt=0, example=1, description="Valid Product ID (must be > 0)")
    quantity: int = Field(..., ge=0, example=50, description="Stock quantity (must be >= 0)")


class StockUpdate(BaseModel):
    quantity: int = Field(..., ge=0, example=100, description="Updated stock quantity (must be >= 0)")


class Stock(BaseModel):
    id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True
