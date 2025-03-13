from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

# Create a router for product-related endpoints
router = APIRouter()


@router.post("/products/", response_model=schemas.Product)
def create_product_endpoint(
        product: schemas.ProductCreate, db: Session = Depends(database.get_db)
):
    return crud.create_product(db, product)


@router.get("/products/", response_model=list[schemas.Product])
def get_products_endpoint(
        skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)
):
    return crud.get_products(db, skip=skip, limit=limit)


@router.get("/products/{product_id}", response_model=schemas.Product)
def get_product_endpoint(product_id: int, db: Session = Depends(database.get_db)):
    db_product = crud.get_product_by_id(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


#
@router.put("/products/{product_id}", response_model=schemas.Product)
def update_product_endpoint(
        product_id: int,
        product_update: schemas.ProductUpdate,
        db: Session = Depends(database.get_db)
):
    db_product = crud.update_product(db, product_id, product_update)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


@router.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product_endpoint(product_id: int, db: Session = Depends(database.get_db)):
    db_product = crud.delete_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product
