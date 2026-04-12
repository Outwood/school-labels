"""Label generator core functionality."""

import csv
from pathlib import Path
from typing import Any, TextIO

from .templates import (
    EmailPasswordTemplate,
    LabelTemplate,
)

TEMPLATES: dict[str, LabelTemplate] = {
    t.name: t
    for t in [
        EmailPasswordTemplate(),
    ]
}


def detect_template(columns: list[str]) -> LabelTemplate | None:
    """Auto-detect template based on CSV columns."""
    for template in TEMPLATES.values():
        if all(col in columns for col in template.required_columns):
            return template
    return None


def generate_filename(base_filename: str, max_attempts: int = 1000) -> str:
    """Generate output filename with conflict resolution."""
    path = Path(base_filename)
    if not path.exists():
        return base_filename

    for counter in range(1, max_attempts + 1):
        candidate = path.with_stem(f"{path.stem}-{counter}")
        if not candidate.exists():
            return str(candidate)
    msg = f"Could not find available filename after {max_attempts} attempts"
    raise RuntimeError(msg)


def read_csv_data(input_file: TextIO) -> list[dict[str, Any]]:
    """Read CSV data from file or stdin."""
    reader = csv.DictReader(input_file)
    return list(reader)


def validate_columns(data: list[dict[str, Any]], template: LabelTemplate) -> list[str]:
    """Check that required columns are present. Returns list of missing columns."""
    if not data:
        return []
    present = set(data[0].keys())
    return [col for col in template.required_columns if col not in present]


def generate_labels(
    data: list[dict[str, Any]], style: str, *, break_column: str | None = None
) -> bytes:
    """Generate labels PDF and return as bytes.

    Args:
        data: List of row dicts, one per label.
        style: Template name (e.g. ``"email-password"``). Must be a key in
            :data:`TEMPLATES`.
        break_column: Column name that triggers a page break on value change.

    Returns:
        Raw PDF bytes.

    Raises:
        ValueError: If ``style`` is not a recognised template name.
    """
    template = TEMPLATES.get(style)
    if template is None:
        valid = list(TEMPLATES)
        msg = f"Unknown style {style!r}. Valid styles: {valid}"
        raise ValueError(msg)
    raw = template.create_pdf(data, break_column).output()
    if raw is None:
        msg = "FPDF.output() unexpectedly returned None"
        raise RuntimeError(msg)
    return bytes(raw)
