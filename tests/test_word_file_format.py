import pytest

from app.services.word_file_format import parse_line


@pytest.mark.parametrize(
    "line,expected",
    [
        ("apple;jabłko", ("apple", "jabłko")),
        ("  Apple ; Jabłko ", ("apple", "jabłko")),
        ("English;Polish", None),
        ("angielski;polski", None),
        ("", None),
        ("no-separator", None),
        ("onlyone;", None),
        (";onlytwo", None),
    ],
)
def test_parse_line(line: str, expected: tuple[str, str] | None) -> None:
    assert parse_line(line) == expected
