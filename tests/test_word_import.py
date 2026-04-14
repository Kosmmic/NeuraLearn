from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.services.word_import import import_fiszki_from_path
from models import Base, Fish_lists, Fiszka, Lists


@pytest.fixture
def db_session():
    """Izolowana baza w pamięci — bez globalnego ``memory.db`` aplikacji."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    sess = Session()
    try:
        yield sess
    finally:
        sess.close()


def test_import_adds_cards_and_counts(tmp_path: Path, db_session) -> None:
    f = tmp_path / "w.txt"
    f.write_text(
        "english;polish\nfoo;bar\nfoo;bar\nbad\nbaz;qux\n",
        encoding="utf-8",
    )
    r = import_fiszki_from_path(db_session, f)
    assert r.added == 2
    assert r.skipped_duplicate == 1
    assert r.skipped_unparsed == 1
    rows = db_session.query(Fiszka).order_by(Fiszka.question).all()
    assert [(x.question, x.answer) for x in rows] == [("baz", "qux"), ("foo", "bar")]


def test_import_with_list_name(tmp_path: Path, db_session) -> None:
    f = tmp_path / "w.txt"
    f.write_text("a;b\nc;d\n", encoding="utf-8")
    r = import_fiszki_from_path(db_session, f, list_name="Lista A")
    assert r.added == 2
    lst = db_session.query(Lists).filter_by(name="Lista A").one()
    links = db_session.query(Fish_lists).filter_by(list_id=lst.id).all()
    assert len(links) == 2


def test_import_swapped_columns(tmp_path: Path, db_session) -> None:
    """Gdy pierwsza kolumna to PL: ``english_as_question=False`` zamienia kolumny przy zapisie."""
    f = tmp_path / "w.txt"
    f.write_text("english;polish\nkot;cat\n", encoding="utf-8")
    r = import_fiszki_from_path(db_session, f, english_as_question=False)
    assert r.added == 1
    card = db_session.query(Fiszka).one()
    assert card.question == "cat"
    assert card.answer == "kot"


def test_import_uses_fixture_file(db_session) -> None:
    root = Path(__file__).resolve().parent
    fixture = root / "fixtures" / "sample_words.txt"
    r = import_fiszki_from_path(db_session, fixture, list_name="L")
    assert r.added == 2
    assert r.skipped_duplicate == 1
    assert r.skipped_unparsed == 1
