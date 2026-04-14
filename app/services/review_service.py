from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Session

from app.domain.scheduling import schedule_next_review
from db_crud import ProgressCRUD, ReviewLogsCRUD
from models import Progress


def derive_grade(*, is_correct: int, response_time_ms: int) -> int:
    if is_correct not in (0, 1):
        raise ValueError("is_correct musi być 0 lub 1")
    if response_time_ms < 0:
        raise ValueError("response_time_ms nie może być ujemny")
    if is_correct == 0:
        return 1
    if response_time_ms <= 3000:
        return 5
    if response_time_ms <= 7000:
        return 4
    return 3


class ReviewService:
    def __init__(self, db_session: Session):
        self._db = db_session
        self._progress = ProgressCRUD(db_session)
        self._logs = ReviewLogsCRUD(db_session)

    def register_review(
        self,
        *,
        user_id: int,
        fiszka_id: int,
        session_id: int,
        is_correct: int,
        response_time_ms: int,
    ) -> Progress:

        if response_time_ms < 0:
            raise ValueError("response_time_ms nie może być ujemny")

        progress = (
            self._db.query(Progress)
            .filter_by(user_id=user_id, fiszka_id=fiszka_id)
            .first()
        )

        if progress is None:
            progress = self._progress.dodaj(
                user_id=user_id,
                fiszka_id=fiszka_id,
                mastery_level=0,
                review_date=None,
            )
        now = datetime.now()
        grade = derive_grade(is_correct=is_correct, response_time_ms=response_time_ms)

        sched = schedule_next_review(
            current_mastery_level=progress.mastery_level or 0,
            grade=grade,
            now=now,
        )

        self._logs.dodaj(
            user_id=user_id,
            fiszka_id=fiszka_id,
            session_id=session_id,
            grade=grade,
            response_time_ms=response_time_ms,
            created_at=now,
        )

        self._progress.edytuj(
            progress.id,
            mastery_level=sched.new_mastery_level,
            review_date=sched.next_review_date,
        )

        self._db.refresh(progress)
        return progress
