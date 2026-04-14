from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationResult:
    is_correct: int
    score: float


def normalize_text(s: str) -> str:
    return " ".join((s or "").strip().lower().split())


def validate_answer(user_answer: str, expected_answer: str) -> ValidationResult:
    ua = normalize_text(user_answer)
    ea = normalize_text(expected_answer)

    ok = int(ua == ea)
    return ValidationResult(is_correct=ok, score=float(ok))
