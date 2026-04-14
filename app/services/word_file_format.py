from __future__ import annotations

# Linie uznawane za nagłówek (ignorowane przy imporcie), porównanie case-insensitive.
HEADER_LINES = frozenset({"english;polish", "angielski;polski"})


def normalize_text(s: str) -> str:
    return (s or "").strip().lower()


def parse_line(line: str) -> tuple[str, str] | None:
    line = line.strip()
    if not line or ";" not in line:
        return None
    if line.lower() in HEADER_LINES:
        return None
    left, right = line.split(";", 1)
    left_n, right_n = normalize_text(left), normalize_text(right)
    if not left_n or not right_n:
        return None
    return left_n, right_n
