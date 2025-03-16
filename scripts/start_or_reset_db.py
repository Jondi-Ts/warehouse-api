import os
import sys
import sqlite3

# ✅ Get the absolute path of the project root
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "/..")
sys.path.insert(0, PROJECT_ROOT)  # ✅ Ensure Python looks for modules in the root directory

from sqlalchemy.orm import Session
from app.database import engine, Base
from alembic.config import Config
from alembic import command

# ✅ Define database path
db_path = os.path.join(PROJECT_ROOT, "database.db")

# ✅ Step 1: Close any open SQLite connections
try:
    conn = sqlite3.connect(db_path)
    conn.close()
except Exception as e:
    print(f"Warning: Could not close database connection. Error: {e}")

# ✅ Step 2: Check if database exists and delete (if needed)
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print("Existing database deleted!")
    except PermissionError as e:
        print(f"ERROR: Could not delete database. It is in use by another process. ({e})")
        sys.exit(1)
else:
    print("Database does not exist. Creating a new one...")

# ✅ Step 3: Create new tables based on SQLAlchemy models
Base.metadata.create_all(bind=engine)
print("Database tables created!")

# ✅ Step 4: Apply Alembic migrations
alembic_cfg = Config(os.path.join(PROJECT_ROOT, "alembic.ini"))
command.upgrade(alembic_cfg, "head")
print("Migrations applied successfully!")
