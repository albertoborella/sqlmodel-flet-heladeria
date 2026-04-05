from sqlmodel import Session, select
from database.database import engine
from models.stock_model import Gusto


def cargar_gustos_iniciales():
    gustos = [
        {"nombre": "Chocolate", "peso_balde": 5},
        {"nombre": "Vainilla", "peso_balde": 5},
        {"nombre": "Frutilla", "peso_balde": 5},
    ]

    with Session(engine) as session:
        existe = session.exec(select(Gusto)).first()

        if existe:
            return

        for g in gustos:
            session.add(Gusto(**g))

        session.commit()