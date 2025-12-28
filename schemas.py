import datetime

from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    summary: str
    publication_date: datetime.date | None


class BookCreate(BookBase):
    authors_id: list[int]


class BookUpdate(BookBase):
    authors_id: list[int]


class Book(BookBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    authors: list["AuthorName"]


class BookName(BaseModel):
    title: str


class BookId(BaseModel):
    id: str


class AuthorBase(BaseModel):
    name: str
    bio: str


class AuthorCreate(AuthorBase):
    books_id: list[int]


class AuthorUpdate(AuthorBase):
    books_id: list[int]


class Author(AuthorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    books: list[BookName]


class AuthorName(BaseModel):
    name: str
