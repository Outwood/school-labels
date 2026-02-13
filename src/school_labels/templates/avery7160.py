"""Base template for Avery 7160 label sheets."""

from abc import ABC, abstractmethod
from typing import Any, override

from fpdf import FPDF

from .base import LabelTemplate


class Avery7160Template(LabelTemplate, ABC):
    """Base class for Avery 7160 label templates."""

    # Avery 7160 specifications (in mm)
    SHEET_WIDTH: float = 210  # A4 width
    SHEET_HEIGHT: float = 297  # A4 height
    LABEL_WIDTH: float = 63.5
    LABEL_HEIGHT: float = 38.1
    LABELS_PER_ROW: int = 3
    LABELS_PER_COL: int = 7
    LEFT_MARGIN: float = 7.25
    TOP_MARGIN: float = 15.15
    H_SPACING: float = 2.5
    V_SPACING: float = 0

    LABELS_PER_PAGE: int = LABELS_PER_ROW * LABELS_PER_COL

    def _setup_pdf(self) -> FPDF:
        """Setup PDF with A4 page size."""
        pdf = FPDF()
        pdf.set_title(self.pdf_title)
        pdf.c_margin = 0
        pdf.add_page()
        pdf.set_auto_page_break(False)
        return pdf

    def _get_label_position(self, label_index: int) -> tuple[float, float]:
        """Get x, y position for label at given index on current page."""
        row = label_index // self.LABELS_PER_ROW
        col = label_index % self.LABELS_PER_ROW

        x = self.LEFT_MARGIN + col * (self.LABEL_WIDTH + self.H_SPACING)
        y = self.TOP_MARGIN + row * (self.LABEL_HEIGHT + self.V_SPACING)

        return x, y

    @abstractmethod
    def _draw_label_content(self, pdf: FPDF, x: float, y: float, data: dict[str, Any]):
        """Draw content for a single label."""

    @override
    def create_pdf(
        self, data: list[dict[str, Any]], break_column: str | None = None
    ) -> FPDF:
        """Create PDF with labels using Avery 7160 layout."""
        pdf = self._setup_pdf()
        label_count = 0
        last_break_value = None

        for row in data:
            # Check for page break on column value change
            if break_column and break_column in row:
                current_break_value = row[break_column]
                if (
                    last_break_value is not None
                    and current_break_value != last_break_value
                ):
                    pdf.add_page()
                    label_count = 0
                last_break_value = current_break_value

            # Add new page if current page is full (skip if break already added a fresh page)
            if label_count > 0 and label_count % self.LABELS_PER_PAGE == 0:
                pdf.add_page()

            # Get position for current label
            page_label_index = label_count % self.LABELS_PER_PAGE
            x, y = self._get_label_position(page_label_index)

            self._draw_label_content(pdf, x, y, row)
            label_count += 1

        return pdf
