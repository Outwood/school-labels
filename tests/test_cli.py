"""Tests for CLI integration."""

import io
import os

from school_labels.cli import main


class TestCli:
    def test_with_file(self, email_csv_path, tmp_path):
        output = str(tmp_path / "out.pdf")
        result = main([str(email_csv_path), "-o", output])
        assert result == 0
        assert os.path.exists(output)

    def test_stdout(self, email_csv_path, monkeypatch):
        buf = io.BytesIO()
        monkeypatch.setattr("sys.stdout", type("FakeStdout", (), {"buffer": buf})())
        result = main([str(email_csv_path), "--output", "-"])
        assert result == 0
        assert buf.getvalue()[:5] == b"%PDF-"

    def test_explicit_style(self, email_csv_path, tmp_path):
        output = str(tmp_path / "out.pdf")
        result = main([str(email_csv_path), "--style", "email-password", "-o", output])
        assert result == 0
        assert os.path.exists(output)

    def test_missing_file(self, capsys):
        result = main(["nonexistent.csv", "-o", "/dev/null"])
        assert result == 1
        assert "not found" in capsys.readouterr().err

    def test_no_data(self, tmp_path, capsys):
        csv_path = tmp_path / "empty.csv"
        csv_path.write_text("admin,last_name,first_name,group,email,password\n")
        result = main([str(csv_path), "-o", str(tmp_path / "out.pdf")])
        assert result == 1
        assert "No data" in capsys.readouterr().err

    def test_wrong_columns_with_style(self, bad_csv_path, tmp_path, capsys):
        result = main(
            [
                str(bad_csv_path),
                "--style",
                "email-password",
                "-o",
                str(tmp_path / "out.pdf"),
            ]
        )
        assert result == 1
        assert "missing required columns" in capsys.readouterr().err

    def test_auto_detect_fails(self, bad_csv_path, tmp_path, capsys):
        result = main([str(bad_csv_path), "-o", str(tmp_path / "out.pdf")])
        assert result == 1
        assert "Could not auto-detect" in capsys.readouterr().err

    def test_break_column(self, email_csv_path, tmp_path):
        output = str(tmp_path / "out.pdf")
        result = main([str(email_csv_path), "--break", "group", "-o", output])
        assert result == 0
        assert os.path.exists(output)
