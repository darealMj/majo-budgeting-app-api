from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


# NOTE: Model imports removed to avoid circular imports
# Models will auto-register when imported elsewhere
# If you need to ensure all models are registered, import them in main.py
