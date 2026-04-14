from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sqlalchemy.orm import Session

from app.services.word_file_format import HEADER_LINES, parse_line
from models import Fish_lists, Fiszka, Lists


@dataclass(frozen=True)
class ImportResult:
    added: int
    skipped_duplicate: int
    skipped_unparsed: int


def import_fiszki_from_path(
    db: Session,
    path: Path | str,
    *,
    list_name: str | None = None,
    english_as_question: bool = True,
) -> ImportResult:
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(p)

    text = p.read_text(encoding="utf-8", errors="replace")
    added = 0
    skipped_duplicate = 0
    skipped_unparsed = 0

    list_obj: Lists | None = None
    if list_name and list_name.strip():
        name = list_name.strip()
        list_obj = db.query(Lists).filter(Lists.name == name).first()
        if list_obj is None:
            list_obj = Lists(name=name, describe="Utworzona przy imporcie z pliku")
            db.add(list_obj)
            db.flush()

    try:
        for raw_line in text.splitlines():
            pair = parse_line(raw_line)
            if pair is None:
                stripped = raw_line.strip()
                if not stripped:
                    continue
                if stripped.lower() in HEADER_LINES:
                    continue
                skipped_unparsed += 1
                continue
            left, right = pair
            question, answer = (left, right) if english_as_question else (right, left)

            exists = db.query(Fiszka).filter(Fiszka.question == question).first()
            if exists:
                skipped_duplicate += 1
                continue

            card = Fiszka(question=question, answer=answer)
            db.add(card)
            db.flush()

            if list_obj is not None:
                link = Fish_lists(list_id=list_obj.id, fiszka_id=card.id)
                db.add(link)

            added += 1

        db.commit()
    except Exception:
        db.rollback()
        raise

    return ImportResult(
        added=added,
        skipped_duplicate=skipped_duplicate,
        skipped_unparsed=skipped_unparsed,
    )
