from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
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
        return f"User o numerze ID: {self.id} (username='{self.username}', name='{self.email}', fullname='{self.password_hash}')>"


class Progres(Base):
    __tablename__ = "progres"

    user_id = Column(Integer, ForeignKey("user.id"), primary_key=True)
    fiszka_id = Column(Integer, ForeignKey("fiska.id"), primary_key=True)

    mastery_level = Column(Integer, default=0)
    review_date = Column(DateTime)


class TrainingSession(Base):
    __tablename__ = "sessions"
    user_id = Column(Integer, foreign_key="users.id")
    start_time = Column(DateTime)
    end_time = Column(DateTime)


class ReviewLogs(Base):
    __tablename__ = "review_logs"
    id = Column(Integer)
    user_id = Column(Integer, foreign_key="users.id")
    fiszka_id = Column(
        Integer,
        foreign_key="fiszka.id",
    )
    session_id = Column(
        Integer,
        foreign_key="sessions.id",
    )
    grade = Column(Integer)
    response_time_ms = Column(Integer)
    created_at = Column(DateTime)


class Fiszka(Base):
    __tablename__ = "fiszka"

    id = Column(Integer, primary_key=True)
    question = Column(String, unique=True)
    answer = Column(String)

    def __repr__(self):
        return f"Fiszka o numerze ID: {self.id} (question='{self.question}', answer='{self.answer}')>"


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    def __repr__(self):
        return f"tag o numerze ID: {self.id} (nazwa= {self.name})"


class List(Base):
    __tablename__ = "list"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    describe = Column(String)

    def __repr__(self):
        return (
            f"lista o numerze ID: {self.id} (nazwa={self.name}, opis= {self.describe})"
        )


class Tag_lists(Base):
    __tablename__ = "tag_lists"
    id_list = Column(Integer, foreign_key="list.id")
    id_tag = Column(Integer, foreign_key="tag.id")

    def __repr__(self):
        return "lista_tagów o numerze ID: {self.id_list} (id_tagow= {self.id_tag},)"


class Fish_lists(Base):
    __tablename__ = "fiszka_list"
    id_list = Column(Integer, foreign_key="list.id")
    id_fish = Column(Integer, foreign_key="fish.id")

    def __repr__(self):
        return "lista fiszek o numerze id: {self.id_list (id_fiszek={self.id_tag})"


Session = sessionmaker(bind=engine)
session = Session()

if __name__ == "models.py":
    engine = create_engine("sqlite:///memory.db")
    Base.metadata.create_all(engine)
