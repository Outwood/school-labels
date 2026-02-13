"""Email password labels template for Avery 7160."""

from typing import Any, override

from fpdf import FPDF

from .avery7160 import Avery7160Template


class EmailPasswordTemplate(Avery7160Template):
    """Email password labels template."""

    H_PADDING: float = 2.8
    V_PADDING: float = 4.2

    @property
    @override
    def name(self) -> str:
        return "email-password"

    @property
    @override
    def required_columns(self) -> list[str]:
        return ["admin", "last_name", "first_name", "group", "email", "password"]

    @property
    @override
    def pdf_title(self) -> str:
        return "Account stickers"

    @override
    def _draw_label_content(self, pdf: FPDF, x: float, y: float, data: dict[str, Any]):
        """Draw email and password labels."""
        full_width = self.LABEL_WIDTH - (2 * self.H_PADDING)
        col1 = int(full_width / 3) - 1
        col2 = (col1 * 2) - 1

        # Starting position with padding
        content_x = x + self.H_PADDING
        current_y = y + self.V_PADDING

        # Name section
        pdf.set_xy(content_x, current_y)
        pdf.set_font("Helvetica", "", 11)
        name_text = f"{data.get('first_name', '')} {data.get('last_name', '')}"
        pdf.cell(full_width, 4.2, self._fit_text(pdf, name_text, full_width))

        # Horizontal line (spans full label width)
        current_y += 4.4
        pdf.line(x, current_y, x + self.LABEL_WIDTH, current_y)

        # Move down after line
        current_y += 2.1  # 6pt ≈ 2.1mm

        # Admin no. and Group labels (7pt font)
        pdf.set_font("Helvetica", "", 7)
        pdf.set_xy(content_x, current_y)
        pdf.cell(col1, 2.8, "Admin no.")  # 8pt height ≈ 2.8mm
        pdf.set_xy(content_x + full_width - col2, current_y)
        pdf.cell(col2, 2.8, "Group")

        # Move down for values
        current_y += 3.2  # 9pt ≈ 3.2mm

        # Admin and Group values
        pdf.set_font("Helvetica", "", 11)
        pdf.set_xy(content_x, current_y)
        admin_text = data.get("admin", "")
        pdf.cell(col1, 3.5, self._fit_text(pdf, admin_text, col1))
        pdf.set_xy(content_x + full_width - col2, current_y)
        group_text = data.get("group", "")
        pdf.cell(col2, 3.5, self._fit_text(pdf, group_text, col2))

        # Move down
        current_y += 5.6  # 16pt ≈ 5.6mm

        # Email label
        pdf.set_font("Helvetica", "", 7)
        pdf.set_xy(content_x, current_y)
        pdf.cell(full_width, 2.8, "Email")

        # Move down for email value
        current_y += 3.2  # 9pt ≈ 3.2mm

        # Email value
        pdf.set_font("Helvetica", "", 11)
        pdf.set_xy(content_x, current_y)
        email_text = data.get("email", "")
        pdf.cell(full_width, 4.2, self._shrink_text(pdf, email_text, full_width))

        # Move down
        current_y += 5.6  # 16pt ≈ 5.6mm

        # Password label
        pdf.set_font("Helvetica", "", 7)
        pdf.set_xy(content_x, current_y)
        password_label = "Password"
        pdf.cell(full_width, 2.8, password_label)

        # Move down for password value
        current_y += 3.2  # 9pt ≈ 3.2mm

        # Password value (using Courier font like Ruby template)
        pdf.set_font("Courier", "", 11)
        pdf.set_xy(content_x, current_y)
        password_text = data.get("password", "")
        pdf.cell(full_width, 4.2, self._shrink_text(pdf, password_text, full_width))
