"""Декларативный класс базы данных приложения."""

from sqlalchemy.orm import DeclarativeBase


class FiresDB(DeclarativeBase):
    """База данных приложения."""
