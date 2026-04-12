from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///memory.db", echo=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)
    password_hash = Column(String)

    def __repr__(self):
        return f"User o numerze ID: {self.id} (username='{self.username}', email='{self.email}', password_hash='{self.password_hash}')"


class Progress(Base):
    __tablename__ = "progress"
    __table_args__ = (UniqueConstraint("user_id", "fiszka_id", name="uq_progress_user_fiszka"),)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fiszka_id = Column(Integer, ForeignKey("fiszka.id"), nullable=False)
    mastery_level = Column(Integer, default=0)
    review_date = Column(DateTime)
    def __repr__(self):
        return f"Progress o numerze ID: {self.id} (user_id='{self.user_id}', fiszka_id='{self.fiszka_id}', mastery_level='{self.mastery_level}', review_date='{self.review_date}')"

class TrainingSession(Base):
    __tablename__ = "sessions"
    __table_args__ = (UniqueConstraint("user_id", "start_time", name="uq_session_user_start_time"),)
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    def __repr__(self):
        return f"TrainingSession o numerze ID: {self.id} (user_id='{self.user_id}', start_time='{self.start_time}', end_time='{self.end_time}')"

class ReviewLogs(Base):
    __tablename__ = "review_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    fiszka_id = Column(
        Integer,
        ForeignKey("fiszka.id"),
    )
    session_id = Column(
        Integer,
        ForeignKey("sessions.id"),
    )
    grade = Column(Integer)
    response_time_ms = Column(Integer)
    created_at = Column(DateTime)
    def __repr__(self):
        return f"ReviewLogs o numerze ID: {self.id} (user_id='{self.user_id}', fiszka_id='{self.fiszka_id}', session_id='{self.session_id}', grade='{self.grade}', response_time_ms='{self.response_time_ms}', created_at='{self.created_at}')"

class Fiszka(Base):
    __tablename__ = "fiszka"

    id = Column(Integer, primary_key=True)
    question = Column(String, unique=True)
    answer = Column(String)

    def __repr__(self):
        return f"Fiszka o numerze ID: {self.id} (question='{self.question}', answer='{self.answer}')"


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return f"tag o numerze ID: {self.id} (nazwa= {self.name})"


class Lists(Base):
    __tablename__ = "lists"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    describe = Column(String)

    def __repr__(self):
        return (
            f"lista o numerze ID: {self.id} (nazwa={self.name}, opis= {self.describe})"
        )


class Tag_lists(Base):
    __tablename__ = "tag_lists"
    list_id = Column(Integer, ForeignKey("lists.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True)

    def __repr__(self):
        return f"lista_tagów o numerze ID: {self.list_id} (id_tagow= {self.tag_id})"


class Fish_lists(Base):
    __tablename__ = "fiszka_list"
    list_id = Column(Integer, ForeignKey("lists.id"), primary_key=True)
    fiszka_id = Column(Integer, ForeignKey("fiszka.id"), primary_key=True)

    def __repr__(self):
        return f"lista fiszek o numerze id: {self.list_id} (id_fiszek={self.fiszka_id})"


Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "__main__":
    engine = create_engine("sqlite:///memory.db")
    Base.metadata.create_all(engine)
