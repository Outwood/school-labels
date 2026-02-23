"""Tests for label templates."""

from fpdf import FPDF

from school_labels.templates import (
    AttendanceTemplate,
    Avery7160Template,
    EmailPasswordTemplate,
    LabelTemplate,
)


class TestLabelTemplateTextHelpers:
    def test_fit_text_short(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "", 11)
        result = LabelTemplate._fit_text(pdf, "Short", 60.0)
        assert result == "Short"

    def test_fit_text_long(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "", 11)
        long_name = "Bartholomew Wolfeschlegelsteinhausenbergerdorff"
        result = LabelTemplate._fit_text(pdf, long_name, 30.0)
        assert result.endswith("...")
        assert len(result) < len(long_name)
        assert pdf.get_string_width(result) <= 30.0

    def test_shrink_text_short(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "", 11)
        result = LabelTemplate._shrink_text(pdf, "Short", 60.0)
        assert result == "Short"
        assert pdf.font_size_pt == 11

    def test_shrink_text_long(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", "", 11)
        long_email = "bartholomew.wolfeschlegelstein@schoolname.org.uk"
        result = LabelTemplate._shrink_text(pdf, long_email, 30.0)
        assert result == long_email
        assert pdf.font_size_pt < 11
        assert pdf.get_string_width(long_email) <= 30.0


class TestAvery7160Layout:
    template = EmailPasswordTemplate()

    def test_label_position_first(self):
        x, y = self.template._get_label_position(0)
        assert x == 7.25
        assert y == 15.15

    def test_label_position_second_col(self):
        x, y = self.template._get_label_position(1)
        assert x == 7.25 + (63.5 + 2.5)
        assert y == 15.15

    def test_label_position_second_row(self):
        x, y = self.template._get_label_position(3)
        assert x == 7.25
        assert y == 15.15 + 38.1

    def test_label_position_last(self):
        x, y = self.template._get_label_position(20)
        assert x == 7.25 + 2 * (63.5 + 2.5)
        assert y == 15.15 + 6 * 38.1

    def test_labels_per_page(self):
        assert Avery7160Template.LABELS_PER_PAGE == 21


class TestEmailPasswordTemplate:
    template = EmailPasswordTemplate()

    def test_name(self):
        assert self.template.name == "email-password"

    def test_required_columns(self):
        assert self.template.required_columns == [
            "admin",
            "last_name",
            "first_name",
            "group",
            "email",
            "password",
        ]

    def test_create_pdf_returns_fpdf(self):
        data = [
            {
                "admin": "1",
                "last_name": "S",
                "first_name": "J",
                "group": "7A",
                "email": "e@x",
                "password": "p",
            }
        ]
        result = self.template.create_pdf(data)
        assert isinstance(result, FPDF)

    def test_create_pdf_single_page(self):
        row = {
            "admin": "1",
            "last_name": "S",
            "first_name": "J",
            "group": "7A",
            "email": "e@x",
            "password": "p",
        }
        data = [row] * 21
        pdf = self.template.create_pdf(data)
        assert pdf.pages_count == 1

    def test_create_pdf_two_pages(self):
        row = {
            "admin": "1",
            "last_name": "S",
            "first_name": "J",
            "group": "7A",
            "email": "e@x",
            "password": "p",
        }
        data = [row] * 22
        pdf = self.template.create_pdf(data)
        assert pdf.pages_count == 2

    def test_create_pdf_contains_name(self):
        data = [
            {
                "admin": "1",
                "last_name": "Smith",
                "first_name": "John",
                "group": "7A",
                "email": "e@x",
                "password": "p",
            }
        ]
        pdf = self.template.create_pdf(data)
        pdf.compress = False
        output = pdf.output()
        assert b"John Smith" in output

    def test_create_pdf_break_column(self):
        row_a = {
            "admin": "1",
            "last_name": "S",
            "first_name": "J",
            "group": "7A",
            "email": "e@x",
            "password": "p",
        }
        row_b = {
            "admin": "2",
            "last_name": "B",
            "first_name": "B",
            "group": "7B",
            "email": "b@x",
            "password": "q",
        }
        data = [row_a, row_b]
        pdf = self.template.create_pdf(data, break_column="group")
        assert pdf.pages_count == 2


class TestAttendanceTemplate:
    template = AttendanceTemplate()
    _sample_row = {
        "admin": "1001",
        "first_name": "John",
        "last_name": "Smith",
        "group": "7A",
        "attendance": "95.50%",
        "trend": "up",
        "colour": "gold",
    }

    def test_name(self):
        assert self.template.name == "attendance"

    def test_required_columns(self):
        assert self.template.required_columns == [
            "admin",
            "first_name",
            "last_name",
            "group",
            "attendance",
            "trend",
            "colour",
        ]

    def test_create_pdf_contains_name(self):
        pdf = self.template.create_pdf([self._sample_row])
        pdf.compress = False
        output = pdf.output()
        assert b"John Smith" in output

    def test_create_pdf_contains_attendance(self):
        pdf = self.template.create_pdf([self._sample_row])
        pdf.compress = False
        output = pdf.output()
        assert b"95.50%" in output

    def test_create_pdf_contains_trend(self):
        pdf = self.template.create_pdf([self._sample_row])
        pdf.compress = False
        output = pdf.output()
        assert b"Up from previous week" in output

    def test_create_pdf_contains_colour_banner(self):
        pdf = self.template.create_pdf([self._sample_row])
        pdf.compress = False
        output = pdf.output()
        assert b"Gold attendance" in output

    def test_create_pdf_empty_trend(self):
        row = {**self._sample_row, "trend": ""}
        pdf = self.template.create_pdf([row])
        pdf.compress = False
        output = pdf.output()
        assert b"previous week" not in output
