from datetime import datetime

from sqlalchemy.orm import Session

from db_crud import TrainingSessionCRUD


class TrainingSessionService:
    def __init__(self, db_session: Session):
        self._training_sessions = TrainingSessionCRUD(db_session)

    def start_training_session(self, user_id: int) -> int:
        row = self._training_sessions.nowa_sesja(
            user_id=user_id, start_time=datetime.now()
        )
        return row.id

    def end_training_session(self, training_session_id: int) -> bool:
        return self._training_sessions.zakoncz_sesja(
            training_session_id, end_time=datetime.now()
        )
