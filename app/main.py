from fastapi import FastAPI
from app.routes import products  # ✅ Import product routes
from app.database import engine, Base

#  Ensure database tables are created before starting
Base.metadata.create_all(bind=engine)

#  Initialize FastAPI app
app = FastAPI(title="Warehouse API")

#  Register product routes
app.include_router(products.router)
