import os
import sys
import sqlite3

# ✅ Get the absolute path of the project root
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "/..")
sys.path.insert(0, PROJECT_ROOT)  # ✅ Tell Python to look for modules in the root directory

from sqlalchemy.orm import Session
from app.database import engine, Base
from alembic.config import Config
from alembic import command

# ✅ Step 1: Close any open SQLite connections before deleting
try:
    conn = sqlite3.connect(os.path.join(PROJECT_ROOT, "database.db"))
    conn.close()  # ✅ Ensures all SQLite connections are closed
except Exception as e:
    print(f"Warning: Could not close database connection. Error: {e}")

# ✅ Step 2: Delete existing database
db_path = os.path.join(PROJECT_ROOT, "database.db")
if os.path.exists(db_path):
    try:
        os.remove(db_path)
        print("Database deleted!")
    except PermissionError as e:
        print(f"ERROR: Could not delete database. It is in use by another process. ({e})")
        sys.exit(1)  # Exit script if deletion fails

# ✅ Step 3: Recreate tables
Base.metadata.create_all(bind=engine)
print("Database tables created!")

# ✅ Step 4: Apply migrations
alembic_cfg = Config(os.path.join(PROJECT_ROOT, "alembic.ini"))  # ✅ Ensure Alembic finds the correct config
command.upgrade(alembic_cfg, "head")
print("Migrations applied successfully!")
