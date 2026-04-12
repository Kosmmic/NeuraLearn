from datetime import datetime
from typing import Generic, Type, TypeVar, Union

from models import (
    Fish_lists,
    Fiszka,
    Lists,
    Progress,
    ReviewLogs,
    Tag,
    Tag_lists,
    TrainingSession,
    User,
)
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseCRUD(Generic[T]):
    def __init__(self, session: Session, model: Type[T]):
        self.session = session
        self.model = model

    def wypisz_wszystkie(self):
        records = self.session.query(self.model).all()
        print(f"All {self.model.__name__}")
        for r in records:
            print(r)

    def dodaj(self, *, verbose: bool = False, **data) -> T:
        try:
            new_obj = self.model(**data)
            self.session.add(new_obj)
            self.session.commit()
            self.session.refresh(new_obj)
            if verbose:
                print(f"Dodano do {self.model.__name__}: {new_obj}")
            return new_obj
        except Exception as e:
            self.session.rollback()
            raise e

    def edytuj(self, id_record: int, *, verbose: bool = False, **data) -> bool:
        try:
            record = self.session.get(self.model, id_record)
            if not record:
                return False
            for key, value in data.items():
                if hasattr(record, key):
                    setattr(record, key, value)
            if verbose:
                print(f"Zaktualizowano {self.model.__name__}: {record}")
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e

    def usun(self, value: Union[int, str], way: str = "id", verbose: bool = False):
        try:
            record = self.session.query(self.model).filter_by(**{way: value}).first()

            if record:
                self.session.delete(record)
                self.session.commit()
                if verbose:
                    print(f"Deleted from {self.model.__name__}: {record}")
                return True

            if verbose:
                print(f"No {self.model.__name__} found with {way}={value}")
            return False
        except Exception as e:
            self.session.rollback()
            raise e

    def pobierz_wszystkie(self, verbose: bool = False) -> list[T]:
        records = self.session.query(self.model).all()
        if verbose:
            print(f"All {self.model.__name__}")
            for r in records:
                print(r)

        return records


class FiszkaCRUD(BaseCRUD[Fiszka]):
    def __init__(self, session: Session):
        super().__init__(session, Fiszka)

    def nowa_fiszka(self, question: str, answer: str, verbose: bool = False):
        return self.dodaj(question=question, answer=answer, verbose=verbose)


class UserCRUD(BaseCRUD[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)


class ProgresCRUD(BaseCRUD[Progress]):
    def __init__(self, session: Session):
        super().__init__(session, Progress)

    def pobierz_dla_uzytkownika(self, user_id: int) -> list[Progress]:
        return self.session.query(Progress).filter(Progress.user_id == user_id).all()


class TrainingSessionCRUD(BaseCRUD[TrainingSession]):
    def __init__(self, session: Session):
        super().__init__(session, TrainingSession)

    def nowa_sesja(self, user_id: int, start_time: datetime, verbose: bool = False):
        return self.dodaj(user_id=user_id, start_time=start_time, verbose=verbose)

    def zakoncz_sesja(self, session_id: int, end_time: datetime, verbose: bool = False):
        return self.edytuj(session_id, end_time=end_time, verbose=verbose)


class ReviewLogsCRUD(BaseCRUD[ReviewLogs]):
    def __init__(self, session: Session):
        super().__init__(session, ReviewLogs)


class TagCRUD(BaseCRUD[Tag]):
    def __init__(self, session: Session):
        super().__init__(session, Tag)


class ListsCRUD(BaseCRUD[Lists]):
    def __init__(self, session: Session):
        super().__init__(session, Lists)


class Tag_listsCRUD(BaseCRUD[Tag_lists]):
    def __init__(self, session: Session):
        super().__init__(session, Tag_lists)


class Fish_listsCRUD(BaseCRUD[Fish_lists]):
    def __init__(self, session: Session):
        super().__init__(session, Fish_lists)
