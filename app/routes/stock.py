from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter()


@router.post("/stock/", response_model=schemas.Stock)
def create_stock_endpoint(stock: schemas.StockCreate, db: Session = Depends(database.get_db)):
    # ✅ Check if the product exists before adding stock
    db_product = crud.get_product_by_id(db, stock.product_id)
    if not db_product:
        raise HTTPException(status_code=400, detail="Product does not exist")

    return crud.create_stock(db, stock)


@router.get("/stock/", response_model=list[schemas.Stock])
def get_stock_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_stock(db, skip=skip, limit=limit)


@router.get("/stock/{product_id}", response_model=schemas.Stock)
def get_stock_by_product_endpoint(product_id: int, db: Session = Depends(database.get_db)):
    db_stock = crud.get_stock_by_product_id(db, product_id)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock entry not found")
    return db_stock


@router.put("/stock/{stock_id}/reduce", response_model=schemas.Stock)
def reduce_stock_endpoint(stock_id: int, quantity: int, db: Session = Depends(database.get_db)):
    db_stock = crud.get_stock_by_id(db, stock_id)
    if not db_stock:
        raise HTTPException(status_code=404, detail="Stock entry not found")

    # ✅ Ensure stock does not go negative
    if db_stock.quantity < quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    db_stock.quantity -= quantity
    db.commit()
    db.refresh(db_stock)
    return db_stock


@router.delete("/stock/{stock_id}", response_model=schemas.Stock)
def delete_stock_endpoint(stock_id: int, db: Session = Depends(database.get_db)):
    db_stock = crud.delete_stock(db, stock_id)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock entry not found")
    return db_stock


@router.get("/stock/below-threshold/", response_model=list[schemas.Stock])
def get_low_stock_products(minimum_quantity: int, db: Session = Depends(database.get_db)):
    return crud.get_products_below_threshold(db, minimum_quantity)
