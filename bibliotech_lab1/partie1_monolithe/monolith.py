"""
BiblioTech - Version 1 : MONOLITHE
-----------------------------------
Tout est regroupé dans UN SEUL fichier : connexion base de données,
modèle, logique métier (CRUD), validation, et interface graphique.
C'est volontaire : c'est exactement ce qui définit un monolithe,
et ce qui en fera les limites (voir README.md).
"""

import sys
from sqlalchemy import create_engine, Column, Integer, String, Float, CheckConstraint
from sqlalchemy.orm import sessionmaker, declarative_base
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)

# ---------------------------------------------------------------------------
# 1. Connexion à PostgreSQL (SQLAlchemy)
# ---------------------------------------------------------------------------
DATABASE_URL = "postgresql://library:library@localhost:5432/library"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ---------------------------------------------------------------------------
# 2. Modèle "Book" (table de la base de données)
# ---------------------------------------------------------------------------
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


# Crée la table si elle n'existe pas encore
Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------------------------
# 3. Logique CRUD (mélangée avec l'accès aux données : typique du monolithe)
# ---------------------------------------------------------------------------
def validate_book_data(available_copies, rental_price):
    """Empêche les valeurs négatives (règle imposée par l'énoncé)."""
    if available_copies < 0:
        raise ValueError("Le nombre d'exemplaires ne peut pas être négatif.")
    if rental_price < 0:
        raise ValueError("Le tarif de location ne peut pas être négatif.")


def create_book(book_id, title, author, available_copies, rental_price):
    validate_book_data(available_copies, rental_price)
    session = SessionLocal()
    try:
        if session.query(Book).filter(Book.id == book_id).first():
            raise ValueError(f"Un livre avec l'ID {book_id} existe déjà.")
        book = Book(
            id=book_id, title=title, author=author,
            available_copies=available_copies, rental_price=rental_price,
        )
        session.add(book)
        session.commit()
    finally:
        session.close()


def get_all_books():
    session = SessionLocal()
    try:
        return session.query(Book).all()
    finally:
        session.close()


def update_book(book_id, title=None, author=None, available_copies=None, rental_price=None):
    session = SessionLocal()
    try:
        book = session.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise ValueError(f"Aucun livre trouvé avec l'ID {book_id}.")
        new_copies = available_copies if available_copies is not None else book.available_copies
        new_price = rental_price if rental_price is not None else book.rental_price
        validate_book_data(new_copies, new_price)

        if title is not None:
            book.title = title
        if author is not None:
            book.author = author
        book.available_copies = new_copies
        book.rental_price = new_price
        session.commit()
    finally:
        session.close()


def delete_book(book_id):
    session = SessionLocal()
    try:
        book = session.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise ValueError(f"Aucun livre trouvé avec l'ID {book_id}.")
        session.delete(book)
        session.commit()
    finally:
        session.close()


# ---------------------------------------------------------------------------
# 4. Interface graphique PyQt5 (couplée directement à la logique métier)
# ---------------------------------------------------------------------------
class LibraryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BiblioTech — Gestion des livres (Monolithe)")
        self.resize(750, 450)
        self._build_ui()
        self.refresh_table()

    def _build_ui(self):
        layout = QVBoxLayout()

        form_layout = QHBoxLayout()
        self.id_input = QLineEdit(placeholderText="ID")
        self.title_input = QLineEdit(placeholderText="Titre")
        self.author_input = QLineEdit(placeholderText="Auteur")
        self.copies_input = QLineEdit(placeholderText="Exemplaires")
        self.price_input = QLineEdit(placeholderText="Tarif")
        for widget in (self.id_input, self.title_input, self.author_input,
                       self.copies_input, self.price_input):
            form_layout.addWidget(widget)
        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        create_btn = QPushButton("Créer")
        update_btn = QPushButton("Modifier")
        delete_btn = QPushButton("Supprimer")
        refresh_btn = QPushButton("Actualiser")
        create_btn.clicked.connect(self.on_create)
        update_btn.clicked.connect(self.on_update)
        delete_btn.clicked.connect(self.on_delete)
        refresh_btn.clicked.connect(self.refresh_table)
        for btn in (create_btn, update_btn, delete_btn, refresh_btn):
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Titre", "Auteur", "Exemplaires", "Tarif"]
        )
        layout.addWidget(self.table)

        self.setLayout(layout)

    def refresh_table(self):
        books = get_all_books()
        self.table.setRowCount(len(books))
        for row, book in enumerate(books):
            self.table.setItem(row, 0, QTableWidgetItem(str(book.id)))
            self.table.setItem(row, 1, QTableWidgetItem(book.title))
            self.table.setItem(row, 2, QTableWidgetItem(book.author))
            self.table.setItem(row, 3, QTableWidgetItem(str(book.available_copies)))
            self.table.setItem(row, 4, QTableWidgetItem(str(book.rental_price)))

    def on_create(self):
        try:
            create_book(
                int(self.id_input.text()),
                self.title_input.text(),
                self.author_input.text(),
                int(self.copies_input.text()),
                float(self.price_input.text()),
            )
            self.refresh_table()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def on_update(self):
        try:
            update_book(
                int(self.id_input.text()),
                title=self.title_input.text() or None,
                author=self.author_input.text() or None,
                available_copies=int(self.copies_input.text()) if self.copies_input.text() else None,
                rental_price=float(self.price_input.text()) if self.price_input.text() else None,
            )
            self.refresh_table()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def on_delete(self):
        try:
            delete_book(int(self.id_input.text()))
            self.refresh_table()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryWindow()
    window.show()
    sys.exit(app.exec_())
