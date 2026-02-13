"""Base template classes for label generation."""

from abc import ABC, abstractmethod
from typing import Any

from fpdf import FPDF


class LabelTemplate(ABC):
    """Base class for label templates."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Template name for CLI selection."""
        pass

    @property
    @abstractmethod
    def required_columns(self) -> list[str]:
        """Required CSV columns for this template."""
        pass

    @property
    @abstractmethod
    def pdf_title(self) -> str:
        """Title for PDF metadata."""
        pass

    @abstractmethod
    def create_pdf(
        self, data: list[dict[str, Any]], break_column: str | None = None
    ) -> FPDF:
        """Create PDF with labels."""
        pass

    @staticmethod
    def _fit_text(pdf: FPDF, text: str, max_width: float) -> str:
        """Truncate text with ellipsis if it exceeds max_width in the current font."""
        text_width = pdf.get_string_width(text)
        if text_width <= max_width:
            return text
        ellipsis = "..."
        ellipsis_width = pdf.get_string_width(ellipsis)
        cut = int(len(text) * (max_width - ellipsis_width) / text_width)
        text = text[:cut]
        while text and pdf.get_string_width(text + ellipsis) > max_width:
            text = text[:-1]
        return text + ellipsis

    @staticmethod
    def _shrink_text(pdf: FPDF, text: str, max_width: float) -> str:
        """Reduce font size so text fits within max_width. Returns text unchanged."""
        text_width = pdf.get_string_width(text)
        if text_width <= max_width:
            return text
        pdf.set_font_size(pdf.font_size_pt * max_width / text_width)
        return text
