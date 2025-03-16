import asyncio
import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import schemas, database
from app.crud.stock_crud import StockCRUD
from app.crud.products_crud import ProductCRUD
from app.task_manager import create_task, update_task_status, run_background_task

logger = logging.getLogger("api_logger")


class StockRouter:
    def __init__(self):
        self.router = APIRouter()
        self.stock_crud_class = StockCRUD
        self.product_crud_class = ProductCRUD

        self.router.add_api_route("/stock/", self.create_stock, methods=["POST"])
        self.router.add_api_route("/stock/", self.get_stock, methods=["GET"])
        self.router.add_api_route("/stock/{product_id}", self.get_stock_by_product_id, methods=["GET"])
        self.router.add_api_route("/stock/{stock_id}/reduce", self.reduce_stock, methods=["PUT"])
        self.router.add_api_route("/stock/{stock_id}/delete", self.delete_stock, methods=["DELETE"])
        self.router.add_api_route("/stock/below-threshold/", self.get_low_stock_products, methods=["GET"])

    def create_stock(self, stock: schemas.StockCreate, db: Session = Depends(database.get_db)):
        """Creates stock entry if product exists."""
        product_crud = self.product_crud_class(db)
        stock_crud = self.stock_crud_class(db)

        db_product = product_crud.get_product_by_id(stock.product_id)
        if not db_product:
            raise HTTPException(status_code=400, detail=f"Cannot add stock: Product ID {stock.product_id} does not exist.")

        return stock_crud.create_stock(stock)

    def get_stock(self, skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
        """Retrieves stock list with pagination."""
        stock_entries = self.stock_crud_class(db).get_stock(skip, limit)
        if not stock_entries:
            raise HTTPException(status_code=404, detail="No stock entries found.")
        return stock_entries

    def get_stock_by_product_id(self, product_id: int, db: Session = Depends(database.get_db)):
        """Retrieves stock by product ID."""
        db_stock = self.stock_crud_class(db).get_stock_by_product_id(product_id)
        if db_stock is None:
            raise HTTPException(status_code=404, detail=f"Stock entry for product ID {product_id} not found.")
        return db_stock

    async def reduce_stock(self, stock_id: int, quantity: int,
                           delay: int = Query(5, ge=1, le=10000),
                           db: Session = Depends(database.get_db)):
        """Starts stock reduction asynchronously without blocking API."""
        stock_crud = self.stock_crud_class(db)
        db_stock = stock_crud.get_stock_by_id(stock_id)

        if not db_stock:
            raise HTTPException(status_code=404, detail="Stock not found.")

        if quantity <= 0 or db_stock.quantity < quantity:
            raise HTTPException(status_code=400, detail=f"Invalid quantity. Available: {db_stock.quantity}")

        # ✅ Generate a task ID
        task_id = create_task()
        logger.info(f"Stock reduction started | Task ID: {task_id} | Delay: {delay}s")

        async def stock_update_logic(task_id, quantity):
            """Handles stock reduction asynchronously with task tracking."""
            try:
                await asyncio.sleep(delay)  # Simulate processing delay
                db_stock.quantity -= quantity  # ✅ Use the passed quantity
                db.commit()
                db.refresh(db_stock)
                update_task_status(task_id, "completed")
                logger.info(f"Task {task_id} completed successfully.")
            except Exception as e:
                db.rollback()
                update_task_status(task_id, "failed")
                logger.error(f"Task {task_id} failed due to error: {str(e)}")

    async def delete_stock(self, stock_id: int,
                           delay: int = Query(5, ge=1, le=10000),
                           db: Session = Depends(database.get_db)):
        """Deletes stock entry asynchronously to handle long operations."""
        stock_crud = self.stock_crud_class(db)
        db_stock = stock_crud.get_stock_by_id(stock_id)

        if not db_stock:
            raise HTTPException(status_code=404, detail=f"Stock entry with ID {stock_id} not found.")

        # ✅ Generate a task ID
        task_id = create_task()
        logger.info(f"Stock deletion started | Task ID: {task_id} | Delay: {delay}s")

        async def delete_logic(task_id):
            """Handles stock deletion asynchronously with task tracking."""
            try:
                await asyncio.sleep(delay)  # Simulate processing delay
                stock_crud.delete_stock(stock_id)
                db.commit()
                update_task_status(task_id, "completed")
                logger.info(f"Task {task_id} completed successfully.")
            except Exception as e:
                db.rollback()
                update_task_status(task_id, "failed")
                logger.error(f"Task {task_id} failed due to error: {str(e)}")

        # ✅ Run the background deletion task
        asyncio.create_task(run_background_task(task_id, delete_logic, task_id))

        return {
            "task_id": task_id,
            "message": "Stock deletion started",
            "expected_time": f"{delay} seconds"
        }

    def get_low_stock_products(self, minimum_quantity: int = 10, db: Session = Depends(database.get_db)):
        """Retrieves all products with low stock (below threshold)."""
        low_stock_products = self.stock_crud_class(db).get_products_below_threshold(minimum_quantity)
        if not low_stock_products:
            raise HTTPException(status_code=404, detail="No low-stock products found.")
        return low_stock_products


def get_stock_router():
    return StockRouter().router
