"""
BiblioTech - Version 3 : SERVICE WEB REST
--------------------------------------------
Même logique métier que la partie SOAP, mais exposée via des endpoints
HTTP classiques (GET/POST/PUT/DELETE) et des payloads JSON, validés par
Pydantic. La documentation (OpenAPI/Swagger) est générée automatiquement.
"""

from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Book
from schemas import BookCreate, BookUpdate, BookOut

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BiblioTech API",
    description="API REST de gestion des livres — Lab SOA, partie 3",
    version="1.0.0",
)


@app.get("/books", response_model=List[BookOut])
def list_books(db: Session = Depends(get_db)):
    """Liste tous les livres."""
    return db.query(Book).all()


@app.get("/books/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Récupère un livre par son ID."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    return book


@app.post("/books", response_model=BookOut, status_code=201)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    """Crée un nouveau livre. Pydantic rejette déjà les valeurs négatives."""
    if db.query(Book).filter(Book.id == payload.id).first():
        raise HTTPException(status_code=400, detail="Cet ID existe déjà")
    book = Book(**payload.model_dump())
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.put("/books/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    """Met à jour un livre existant (champs partiels autorisés)."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Supprime un livre."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    db.delete(book)
    db.commit()
