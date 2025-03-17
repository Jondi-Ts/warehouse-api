## Warehouse API Documentation

### Project Overview

Warehouse API is a FastAPI-based project designed to manage inventory operations efficiently. It supports CRUD
operations for inventory items and integrates an SQL database for persistent storage. The project utilizes Pydantic
models for data validation and SQLAlchemy for database migrations.

### Installation and Setup

#### Steps to Start the Project

1. **Clone the repository:**

   ```sh
   git clone <repository-url>
   cd warehouse-api
   ```

2. **Create a virtual environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   ```sh
   python scripts/start_or_reset_db.py
   ```

   This script will setup a new database or reset it if it already exists.

### Running the Application

Start the FastAPI server by running:

```sh
uvicorn app.main:app --reload
```

This will start the application at [http://127.0.0.1:8000](http://127.0.0.1:8000).

To stop the application, press `CTRL + C` in the terminal.

### API Documentation

The API provides an interactive interface:

- **Swagger UI:** [http://127.0.0.1:8000/docs]
- **ReDoc:** [http://127.0.0.1:8000/redoc]

You can interact with the API using Swagger or directly via the terminal.

### Logging

The application includes a logger that records each API interaction into a log file, stored in the `logs` directory.

### Running Tests

You can run tests in two ways, and pytest generates an HTML report for better readability:

1. **Run the ********************`run_tests.py`******************** script** to execute all tests and generate a report:

   ```sh
   python run_tests.py
   ```

2. **Run tests directly using pytest with no report generation rom tests directory:**

   ```sh
   pytest
   ```



