# Budgeting App API

A FastAPI-based budgeting application backend.

## Setup

1. Clone the repository

2. Create virtual environment:
```
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Run the application:
```
python -m app.main
```

5. Access API docs at: http://localhost:8000/docs

## Project Structure

- app/ - Main application code
- app/core/ - Configuration and security
- app/database/ - Database connection and models
- app/models/ - SQLAlchemy models
- app/schemas/ - Pydantic schemas
- app/api/ - API routes and endpoints
- app/services/ - Business logic layer

## Environment Variables

Copy `.env.example` to `.env` file and update with your settings:
    ```bash
   cp .env.example .env

- DATABASE_URL - Database connection string
- SECRET_KEY - JWT secret key
- CORS_ORIGINS - Allowed CORS origins
