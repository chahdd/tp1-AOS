from typing import Optional
from pydantic import BaseModel, Field


class BookBase(BaseModel):
    title: str
    author: str
    available_copies: int = Field(ge=0, description="Doit être >= 0")
    rental_price: float = Field(ge=0, description="Doit être >= 0")


class BookCreate(BookBase):
    id: int


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    available_copies: Optional[int] = Field(default=None, ge=0)
    rental_price: Optional[float] = Field(default=None, ge=0)


class BookOut(BookBase):
    id: int

    class Config:
        from_attributes = True  # permet de retourner directement un objet SQLAlchemy
