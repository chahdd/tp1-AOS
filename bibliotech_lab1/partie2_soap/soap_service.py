"""
BiblioTech - Version 2 : SERVICE WEB SOAP
------------------------------------------
La logique métier est maintenant exposée via un contrat SOAP formel
(WSDL), au lieu d'être enfermée dans un script + une GUI.
N'importe quel client (Postman, une appli mobile, un autre service)
peut désormais consommer ces opérations, à condition de respecter
l'enveloppe SOAP décrite dans le WSDL.
"""

from spyne import Application, rpc, ServiceBase, Integer, Unicode, Float, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

from sqlalchemy import (
    create_engine, Column, Integer as SAInteger, String,
    Float as SAFloat, CheckConstraint,
)
from sqlalchemy.orm import sessionmaker, declarative_base

# ---------------------------------------------------------------------------
# Connexion DB — même base Postgres que la partie 1
# ---------------------------------------------------------------------------
DATABASE_URL = "postgresql://library:library@localhost:5432/library"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(SAInteger, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    available_copies = Column(SAInteger, nullable=False, default=0)
    rental_price = Column(SAFloat, nullable=False, default=0.0)

    __table_args__ = (
        CheckConstraint("available_copies >= 0", name="check_copies_positive"),
        CheckConstraint("rental_price >= 0", name="check_price_positive"),
    )


Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------------------------
# Type de données du contrat SOAP (apparaît dans le WSDL)
# ---------------------------------------------------------------------------
class BookModel(ComplexModel):
    id = Integer
    title = Unicode
    author = Unicode
    available_copies = Integer
    rental_price = Float


# ---------------------------------------------------------------------------
# Service SOAP : 4 opérations, comme demandé dans l'énoncé
# ---------------------------------------------------------------------------
class LibraryService(ServiceBase):

    @rpc(Integer, Unicode, Unicode, Integer, Float, _returns=Unicode)
    def CreateBook(ctx, id, title, author, available_copies, rental_price):
        if available_copies < 0 or rental_price < 0:
            return "Erreur : exemplaires et tarif doivent être positifs."
        session = SessionLocal()
        try:
            if session.query(Book).filter(Book.id == id).first():
                return f"Erreur : un livre avec l'ID {id} existe déjà."
            book = Book(id=id, title=title, author=author,
                        available_copies=available_copies, rental_price=rental_price)
            session.add(book)
            session.commit()
            return f"Livre '{title}' créé avec succès (ID={id})."
        finally:
            session.close()

    @rpc(Integer, _returns=BookModel)
    def GetBook(ctx, id):
        session = SessionLocal()
        try:
            book = session.query(Book).filter(Book.id == id).first()
            if not book:
                return BookModel(id=id, title="", author="",
                                  available_copies=0, rental_price=0.0)
            return BookModel(
                id=book.id, title=book.title, author=book.author,
                available_copies=book.available_copies,
                rental_price=book.rental_price,
            )
        finally:
            session.close()

    @rpc(Integer, Unicode, Unicode, Integer, Float, _returns=Unicode)
    def UpdateBook(ctx, id, title, author, available_copies, rental_price):
        if available_copies < 0 or rental_price < 0:
            return "Erreur : exemplaires et tarif doivent être positifs."
        session = SessionLocal()
        try:
            book = session.query(Book).filter(Book.id == id).first()
            if not book:
                return f"Erreur : aucun livre avec l'ID {id}."
            book.title = title
            book.author = author
            book.available_copies = available_copies
            book.rental_price = rental_price
            session.commit()
            return f"Livre {id} mis à jour."
        finally:
            session.close()

    @rpc(Integer, _returns=Unicode)
    def DeleteBook(ctx, id):
        session = SessionLocal()
        try:
            book = session.query(Book).filter(Book.id == id).first()
            if not book:
                return f"Erreur : aucun livre avec l'ID {id}."
            session.delete(book)
            session.commit()
            return f"Livre {id} supprimé."
        finally:
            session.close()


application = Application(
    [LibraryService],
    tns="spyne.library.soap",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

wsgi_app = WsgiApplication(application)

if __name__ == "__main__":
    server = make_server("0.0.0.0", 8000, wsgi_app)
    print("Service SOAP démarré sur http://localhost:8000")
    print("WSDL disponible sur       http://localhost:8000/?wsdl")
    server.serve_forever()
