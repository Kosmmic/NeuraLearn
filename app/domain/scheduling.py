from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class SchedulingResult:
    new_mastery_level: int
    next_review_date: datetime


def schedule_next_review(
    *,
    current_mastery_level: int,
    grade: int,
    now: datetime | None = None,
) -> SchedulingResult:
    now = now or datetime.now()

    if grade < 0 or grade > 5:
        raise ValueError("ocena musi byc w zakresie od 0 do 5")

    if grade <= 2:
        new_mastery = 0
        interval_days = 1
    elif grade == 3:
        new_mastery = min(current_mastery_level + 1, 10)
        interval_days = 2
    elif grade == 4:
        new_mastery = min(current_mastery_level + 2, 10)
        interval_days = 4
    else:
        new_mastery = min(current_mastery_level + 3, 10)
        interval_days = 7

    interval_days += max(0, new_mastery // 2)

    return SchedulingResult(
        new_mastery_level=new_mastery,
        next_review_date=now + timedelta(days=interval_days),
    )
