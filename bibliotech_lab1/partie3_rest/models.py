from sqlalchemy import Column, Integer, String, Float, CheckConstraint
from database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    available_copies = Column(Integer, nullable=False, default=0)
    rental_price = Column(Float, nullable=False, default=0.0)

    __table_args__ = (
        CheckConstraint("available_copies >= 0", name="check_copies_positive"),
        CheckConstraint("rental_price >= 0", name="check_price_positive"),
    )
