"""Attendance labels template for Avery 7160."""

from typing import Any, override

from fpdf import FPDF
from fpdf.drawing import DeviceCMYK

from .avery7160 import Avery7160Template

_BLACK = DeviceCMYK(0, 0, 0, 1)
_WHITE = DeviceCMYK(0, 0, 0, 0)


class AttendanceTemplate(Avery7160Template):
    """Attendance labels template."""

    H_PADDING: float = 2.8
    V_PADDING: float = 3.2

    # Banner backgrounds → (fill CMYK, text CMYK)
    COLOUR_MAP: dict[str, tuple[DeviceCMYK, DeviceCMYK]] = {
        "amber": (DeviceCMYK(0, 0.37, 1.0, 0), _BLACK),
        "blue": (DeviceCMYK(0.89, 0.47, 0, 0.25), _WHITE),
        "bronze": (DeviceCMYK(0, 0.38, 0.76, 0.20), _BLACK),
        "coral": (DeviceCMYK(0, 0.56, 0.62, 0), _BLACK),
        "cyan": (DeviceCMYK(1.0, 0.10, 0, 0.35), _WHITE),
        "gold": (DeviceCMYK(0, 0.24, 0.97, 0), _BLACK),
        "green": (DeviceCMYK(0.61, 0, 0.58, 0.44), _WHITE),
        "indigo": (DeviceCMYK(0.70, 0.60, 0, 0.38), _WHITE),
        "lilac": (DeviceCMYK(0.05, 0.32, 0, 0.15), _BLACK),
        "lime": (DeviceCMYK(0.18, 0, 0.77, 0.16), _BLACK),
        "maroon": (DeviceCMYK(0, 0.78, 0.69, 0.53), _WHITE),
        "navy": (DeviceCMYK(1.0, 0.68, 0, 0.62), _WHITE),
        "orange": (DeviceCMYK(0, 0.55, 1.0, 0.06), _BLACK),
        "pink": (DeviceCMYK(0, 0.41, 0.27, 0.04), _BLACK),
        "platinum": (DeviceCMYK(0, 0, 0.01, 0.10), _BLACK),
        "purple": (DeviceCMYK(0.55, 0.75, 0, 0.35), _WHITE),
        "red": (DeviceCMYK(0, 0.80, 0.80, 0.22), _WHITE),
        "silver": (DeviceCMYK(0, 0, 0, 0.26), _BLACK),
        "teal": (DeviceCMYK(1.0, 0, 0.12, 0.53), _WHITE),
        "yellow": (DeviceCMYK(0, 0.15, 0.79, 0.01), _BLACK),
    }

    # Trend key → (display text, text CMYK)
    TREND_MAP: dict[str, tuple[str, DeviceCMYK]] = {
        "up": ("Up from previous week", DeviceCMYK(0.63, 0, 0.60, 0.51)),
        "down": ("Down from previous week", DeviceCMYK(0, 0.80, 0.80, 0.22)),
        "equal": ("Same as previous week", DeviceCMYK(0.63, 0, 0.60, 0.51)),
    }

    @property
    @override
    def name(self) -> str:
        return "attendance"

    @property
    @override
    def pdf_title(self) -> str:
        return "Attendance stickers"

    @property
    @override
    def required_columns(self) -> list[str]:
        return [
            "admin",
            "first_name",
            "last_name",
            "group",
            "attendance",
            "trend",
            "colour",
        ]

    @override
    def _draw_label_content(self, pdf: FPDF, x: float, y: float, data: dict[str, Any]):
        """Draw attendance label content."""
        full_width = self.LABEL_WIDTH - (2 * self.H_PADDING)
        col1 = int(full_width / 3) - 1
        col2 = (col1 * 2) - 1

        content_x = x + self.H_PADDING
        current_y = y + self.V_PADDING

        # Name section — Helvetica 11pt
        pdf.set_xy(content_x, current_y)
        pdf.set_font("Helvetica", "", 11)
        name_text = f"{data.get('first_name', '')} {data.get('last_name', '')}"
        pdf.cell(full_width, 4.2, self._fit_text(pdf, name_text, full_width))

        # Horizontal line (spans full label width)
        current_y += 4.4
        pdf.line(x, current_y, x + self.LABEL_WIDTH, current_y)

        # Gap after line
        current_y += 2.1

        # Admin no. and Group labels (7pt)
        pdf.set_font("Helvetica", "", 7)
        pdf.set_xy(content_x, current_y)
        pdf.cell(col1, 2.8, "Admin no.")
        pdf.set_xy(content_x + full_width - col2, current_y)
        pdf.cell(col2, 2.8, "Group")

        # Admin and Group values (11pt)
        current_y += 3.2
        pdf.set_font("Helvetica", "", 11)
        pdf.set_xy(content_x, current_y)
        admin_text = data.get("admin", "")
        pdf.cell(col1, 3.5, self._fit_text(pdf, admin_text, col1))
        pdf.set_xy(content_x + full_width - col2, current_y)
        group_text = data.get("group", "")
        pdf.cell(col2, 3.5, self._fit_text(pdf, group_text, col2))

        # "School attendance" label (7pt)
        current_y += 5.5
        pdf.set_font("Helvetica", "", 7)
        pdf.set_xy(content_x, current_y)
        pdf.cell(full_width, 2.8, "School attendance")

        # Attendance percentage (left) + Trend text (right) — same line
        current_y += 3.0
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_xy(content_x, current_y)
        raw_attendance = data.get("attendance", "0")
        attendance_val = float(str(raw_attendance).rstrip("%"))
        half_width = full_width / 2
        pdf.cell(half_width, 4.2, f"{attendance_val:.2f}%")

        trend_key = str(data.get("trend", "")).lower()
        if trend_key in self.TREND_MAP:
            trend_text, trend_colour = self.TREND_MAP[trend_key]
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(trend_colour)
            pdf.set_xy(content_x + half_width, current_y)
            pdf.cell(half_width, 4.2, trend_text, align="R")
            pdf.set_text_color(_BLACK)

        # Colour banner — full label width, bottom of label
        current_y += 6.0
        banner_y = current_y
        banner_height = (y + self.LABEL_HEIGHT) - banner_y - 1.75
        colour_key = str(data.get("colour", "")).lower()
        if colour_key in self.COLOUR_MAP:
            bg_colour, txt_colour = self.COLOUR_MAP[colour_key]
            pdf.set_fill_color(bg_colour)
            pdf.rect(x, banner_y, self.LABEL_WIDTH, banner_height, "F")
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(txt_colour)
            pdf.set_xy(x, banner_y)
            banner_text = f"{colour_key.title()} attendance"
            pdf.cell(self.LABEL_WIDTH, banner_height, banner_text, align="C")
            pdf.set_text_color(_BLACK)
