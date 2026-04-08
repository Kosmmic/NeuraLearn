from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///memory.db", echo=False)


class Fiszka(Base):
    __tablename__ = "fiszki"

    id = Column(Integer, primary_key=True)
    question = Column(String, unique=True)
    answer = Column(String)

    def __repr__(self):
        return f"Fiszka o numerze ID: {self.id} (question='{self.question}', answer='{self.answer}')>"


Session = sessionmaker(bind=engine)
session = Session()
