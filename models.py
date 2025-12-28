import datetime
from typing import List

from sqlalchemy import String, Table, Column, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

association_table = Table(
    "association_table",
    Base.metadata,
    Column("author_id", ForeignKey("author.id"), primary_key=True),
    Column("book_id", ForeignKey("book.id"), primary_key=True),
)


class DBBook(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(String(511))
    publication_date: Mapped[datetime.date] = (
        mapped_column(Date(), nullable=True)
    )
    authors: Mapped[List["DBAuthor"]] = (
        relationship(secondary=association_table, back_populates="books")
    )

    def __str__(self):
        return "bool"


class DBAuthor(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, unique=True)
    name: Mapped[str] = mapped_column(String(64))
    bio: Mapped[str] = mapped_column(nullable=True)
    books: Mapped[List[DBBook]] = (
        relationship(secondary=association_table, back_populates="authors")
    )
