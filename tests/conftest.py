"""Shared fixtures for school-labels tests."""

from pathlib import Path

import pytest

EMAIL_CSV_HEADER = "admin,last_name,first_name,group,email,password"
EMAIL_CSV_ROWS = [
    "1001,Smith,John,7A,john.smith@school.org,Pass1234",
    "1002,Jones,Jane,7A,jane.jones@school.org,Pass5678",
    "1003,Brown,Bob,7B,bob.brown@school.org,Pass9012",
]


def _write_csv(path: Path, header: str, rows: list[str]) -> Path:
    path.write_text(header + "\n" + "\n".join(rows) + "\n")
    return path


@pytest.fixture
def email_csv_path(tmp_path):
    return _write_csv(tmp_path / "email.csv", EMAIL_CSV_HEADER, EMAIL_CSV_ROWS)


@pytest.fixture
def bad_csv_path(tmp_path):
    return _write_csv(tmp_path / "bad.csv", "foo,bar,baz", ["1,2,3"])
