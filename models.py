from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


engine = create_engine("sqlite:///memory.db", echo=False)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String)
    password_hash: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return (
            f"User o numerze ID: {self.id} "
            f"(username='{self.username}', email='{self.email}', password_hash='{self.password_hash}')"
        )


class Progress(Base):
    __tablename__ = "progress"
    __table_args__ = (
        UniqueConstraint("user_id", "fiszka_id", name="uq_progress_user_fiszka"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    fiszka_id: Mapped[int] = mapped_column(ForeignKey("fiszka.id"), nullable=False)
    mastery_level: Mapped[int] = mapped_column(Integer, default=0)
    review_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return (
            f"Progress o numerze ID: {self.id} "
            f"(user_id='{self.user_id}', fiszka_id='{self.fiszka_id}', "
            f"mastery_level='{self.mastery_level}', review_date='{self.review_date}')"
        )


class TrainingSession(Base):
    __tablename__ = "sessions"
    __table_args__ = (
        UniqueConstraint("user_id", "start_time", name="uq_session_user_start_time"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return (
            f"TrainingSession o numerze ID: {self.id} "
            f"(user_id='{self.user_id}', start_time='{self.start_time}', end_time='{self.end_time}')"
        )


class ReviewLogs(Base):
    __tablename__ = "review_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    fiszka_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("fiszka.id"), nullable=True
    )
    session_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("sessions.id"), nullable=True
    )
    grade: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    response_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return (
            f"ReviewLogs o numerze ID: {self.id} "
            f"(user_id='{self.user_id}', fiszka_id='{self.fiszka_id}', "
            f"session_id='{self.session_id}', grade='{self.grade}', "
            f"response_time_ms='{self.response_time_ms}', created_at='{self.created_at}')"
        )


class Fiszka(Base):
    __tablename__ = "fiszka"

    id: Mapped[int] = mapped_column(primary_key=True)
    question: Mapped[str] = mapped_column(String, unique=True)
    answer: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"Fiszka o numerze ID: {self.id} (question='{self.question}', answer='{self.answer}')"


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)

    def __repr__(self) -> str:
        return f"tag o numerze ID: {self.id} (nazwa={self.name})"


class Lists(Base):
    __tablename__ = "lists"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    describe: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    def __repr__(self) -> str:
        return (
            f"lista o numerze ID: {self.id} (nazwa={self.name}, opis={self.describe})"
        )


class Tag_lists(Base):
    __tablename__ = "tag_lists"

    list_id: Mapped[int] = mapped_column(ForeignKey("lists.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id"), primary_key=True)

    def __repr__(self) -> str:
        return f"lista_tagów o numerze ID: {self.list_id} (id_tagow={self.tag_id})"


class Fish_lists(Base):
    __tablename__ = "fiszka_list"

    list_id: Mapped[int] = mapped_column(ForeignKey("lists.id"), primary_key=True)
    fiszka_id: Mapped[int] = mapped_column(ForeignKey("fiszka.id"), primary_key=True)

    def __repr__(self) -> str:
        return f"lista fiszek o numerze id: {self.list_id} (id_fiszek={self.fiszka_id})"


Session = sessionmaker(bind=engine)
session = Session()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
