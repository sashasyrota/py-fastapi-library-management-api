from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import schemas
from database import Base
from models import DBAuthor, DBBook


def get_objects_from_db_by_id(
        db: Session,
        ids: list[int],
        db_model: Base.metadata
):
    stmt = select(db_model).where(db_model.id.in_(ids))
    return db.scalars(stmt).all()


def get_authors(
        db: Session,
        ids: list[int] | None,
        page: int
):
    authors_on_page = 2
    if ids:
        return get_objects_from_db_by_id(db=db, ids=ids, db_model=DBAuthor)

    return (db.query(DBAuthor)
            .limit(authors_on_page)
            .offset((page - 1) * authors_on_page)
            .all())


def get_author(author_id: int, db: Session):
    author = db.get(DBAuthor, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


def create_author(
        db: Session,
        author_schema: schemas.AuthorCreate
):
    author_db = DBAuthor(
        name=author_schema.name,
        bio=author_schema.bio,
    )
    books = get_objects_from_db_by_id(
        db=db,
        ids=author_schema.books_id,
        db_model=DBBook
    )
    author_db.books.extend(books)
    db.add(author_db)
    db.commit()
    db.refresh(author_db)
    return author_db


def update_author(
        author_id: int,
        author_schema: schemas.AuthorUpdate,
        db: Session,
):
    author_db = db.get(DBAuthor, author_id)
    if not author_db:
        raise HTTPException(status_code=404, detail="Author not found")
    author_db.name = author_schema.name
    author_db.bio = author_schema.bio
    author_db.books = []
    books = (
        get_objects_from_db_by_id(
            db=db,
            ids=author_schema.books_id,
            db_model=DBBook)
    )
    author_db.books.extend(books)

    db.commit()
    return author_db


def delete_author(
        author_id: int,
        db: Session
):
    author = db.get(DBAuthor, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    db.delete(author)
    db.commit()
    return {"ok": True}


def get_books(db: Session, page: int):
    books_on_page = 2
    return (db.query(DBBook).
            limit(books_on_page).
            offset((page - 1) * books_on_page).all())


def create_book(
        db: Session,
        book_schema: schemas.BookCreate
):
    db_book = DBBook(
        title=book_schema.title,
        summary=book_schema.summary,
        publication_date=book_schema.publication_date
    )
    authors = get_objects_from_db_by_id(db, book_schema.authors_id, DBAuthor)
    db_book.authors.extend(authors)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(book_id, db):
    book_db = db.get(DBBook, book_id)
    if not book_db:
        raise HTTPException(status_code=404, detail="Book not found")
    return book_db


def update_book(book_id, book_schema, db):
    book_db = db.get(DBBook, book_id)
    if not book_db:
        raise HTTPException(status_code=404, detail="Book not found")
    book_db.title = book_schema.title
    book_db.summary = book_schema.summary
    book_db.publication_date = book_schema.publication_date
    authors = get_objects_from_db_by_id(db, book_schema.authors_id, DBAuthor)
    book_db.authors = []
    book_db.authors.extend(authors)
    db.commit()
    return book_db


def delete_book(book_id, db):
    book_db = db.get(DBBook, book_id)
    if not book_db:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book_db)
    db.commit()
    return {"ok": True}
