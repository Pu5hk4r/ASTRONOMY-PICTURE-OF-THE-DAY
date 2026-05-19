"""
WHY a model?

A model is the Python representation of a database table.
SQLAlchemy reads your class definition and knows:
  - what table to create (Alembic uses this for migrations)
  - how to map rows to Python objects
  - what types each column holds

HOW it maps to SQL:
  class Apod → table `apods`
  id: Mapped[int] → INTEGER PRIMARY KEY AUTOINCREMENT
  date: Mapped[date] → DATE NOT NULL UNIQUE
  etc.

The `Mapped[X]` syntax (SQLAlchemy 2.0+) uses Python type hints.
It's cleaner than the old Column(String) syntax and gives you IDE autocomplete.
"""
from datetime import date
from typing import Optional

from sqlalchemy import Date, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class Apod(Base):
    __tablename__ = "apods"

    # WHY surrogate key (id) instead of using date as PK?
    # date is the natural key here, but surrogate integer PKs are faster
    # for foreign key references and joins. We add a UNIQUE constraint on date.

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    url: Mapped[str] = mapped_column(String(2000), nullable=False)
    hdurl: Mapped[Optional[str]]= mapped_column(String(2000), nullable=True)

    # media_type is either "image" or "video"
    # NASA sometimes returns a YouTube video instead of an image
    media_type: Mapped[str] = mapped_column(String(20), nullable=False, default="image")

    copyright: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)


    # Table-level constraints
    # WHY here instead of unique=True on the column?
    # UniqueConstraint at the table level is more explicit and supports
    # multi-column unique constraints if you need them later.
    __table_args__ = (
        UniqueConstraint("date",name ="uq_apod_date"),

    )

    def __repr__(self) -> str:
        return f"<Apod date={self.data} title={self.title[:30]}>"
 