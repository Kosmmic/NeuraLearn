from datetime import datetime

from db_crud import FiszkaCRUD
from models import Fiszka, Progress, User
from sqlalchemy.orm import Session


class DeckBuilder:
    def __init__(self, db_session: Session):
        self._db = db_session
        self._fiszki = FiszkaCRUD(db_session)

    def build_deck(self, user_id: int) -> list[Fiszka]:
        user = self._db.get(User, user_id)
        if user is None:
            raise ValueError(f"Brak użytkownika o id={user_id}")
        rows = self._db.query(Progress).filter(Progress.user_id == user_id).all()
        rows.sort(
            key=lambda p: (
                0 if p.review_date is None else 1,
                p.review_date or datetime.min,
            )
        )
        deck: list[Fiszka] = []
        for p in rows:
            f = self._db.get(Fiszka, p.fiszka_id)
            if f is not None:
                deck.append(f)
        return deck
