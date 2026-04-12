from db_crud import ProgressCRUD
from models import Fiszka, Progress, User
from sqlalchemy.orm import Session


class ProgressService:
    def __init__(self, db_session: Session):
        self._db = db_session
        self._progress = ProgressCRUD(db_session)

    def add_fiszka_for_user(self, user_id: int, fiszka_id: int) -> Progress:
        if self._db.get(User, user_id) is None:
            raise ValueError(f"Brak użytkownika o id={user_id}")
        if self._db.get(Fiszka, fiszka_id) is None:
            raise ValueError(f"Brak fiszki o id={fiszka_id}")

        existing = (
            self._db.query(Progress)
            .filter_by(user_id=user_id, fiszka_id=fiszka_id)
            .first()
        )
        if existing:
            return existing
        return self._progress.dodaj(
            user_id=user_id,
            fiszka_id=fiszka_id,
            mastery_level=0,
            review_date=None,
        )

    def add_all_fiszki_for_user(self, user_id: int) -> tuple[int, int]:
        if self._db.get(User, user_id) is None:
            raise ValueError(f"Brak użytkownika o id={user_id}")
        existing_ids = {
            p.fiszka_id for p in self._progress.pobierz_dla_uzytkownika(user_id)
        }
        all_fiszki = self._db.query(Fiszka).all()
        added = 0
        already = 0
        for f in all_fiszki:
            if f.id in existing_ids:
                already += 1
                continue
            self._progress.dodaj(
                user_id=user_id,
                fiszka_id=f.id,
                mastery_level=0,
                review_date=None,
            )
            added += 1
            existing_ids.add(f.id)
        return added, already
