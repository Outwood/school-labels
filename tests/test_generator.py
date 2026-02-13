"""Tests for generator module."""

import io

import pytest

from school_labels import generator
from school_labels.templates import EmailPasswordTemplate


class TestDetectTemplate:
    def test_email_password(self):
        cols = ["admin", "last_name", "first_name", "group", "email", "password"]
        result = generator.detect_template(cols)
        assert isinstance(result, EmailPasswordTemplate)

    def test_no_match(self):
        cols = ["foo", "bar", "baz"]
        assert generator.detect_template(cols) is None

    def test_extra_columns_still_matches(self):
        cols = [
            "admin",
            "last_name",
            "first_name",
            "group",
            "email",
            "password",
            "extra",
        ]
        result = generator.detect_template(cols)
        assert isinstance(result, EmailPasswordTemplate)


class TestReadCsvData:
    def test_reads_rows(self):
        csv_text = "name,age\nAlice,30\nBob,25\n"
        data = generator.read_csv_data(io.StringIO(csv_text))
        assert len(data) == 2
        assert data[0] == {"name": "Alice", "age": "30"}
        assert data[1] == {"name": "Bob", "age": "25"}

    def test_empty_csv(self):
        csv_text = "name,age\n"
        data = generator.read_csv_data(io.StringIO(csv_text))
        assert data == []


class TestValidateColumns:
    def test_valid(self):
        template = EmailPasswordTemplate()
        data = [
            {
                "admin": "1",
                "last_name": "S",
                "first_name": "J",
                "group": "7A",
                "email": "e",
                "password": "p",
            }
        ]
        assert generator.validate_columns(data, template) == []

    def test_missing(self):
        template = EmailPasswordTemplate()
        data = [{"admin": "1", "last_name": "S"}]
        missing = generator.validate_columns(data, template)
        assert "first_name" in missing
        assert "email" in missing
        assert "password" in missing
        assert "group" in missing

    def test_empty_data(self):
        template = EmailPasswordTemplate()
        assert generator.validate_columns([], template) == []


class TestGenerateFilename:
    def test_no_conflict(self, tmp_path):
        path = str(tmp_path / "labels.pdf")
        assert generator.generate_filename(path) == path

    def test_with_conflict(self, tmp_path):
        path = str(tmp_path / "labels.pdf")
        open(path, "w").close()
        result = generator.generate_filename(path)
        assert result == str(tmp_path / "labels-1.pdf")

    def test_max_attempts(self, tmp_path):
        path = str(tmp_path / "labels.pdf")
        open(path, "w").close()
        for i in range(1, 4):
            open(str(tmp_path / f"labels-{i}.pdf"), "w").close()
        with pytest.raises(RuntimeError):
            generator.generate_filename(path, max_attempts=3)
