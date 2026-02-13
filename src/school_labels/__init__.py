"""Outwood Labels - PDF label generation tool for schools."""

from .generator import (
    TEMPLATES,
    detect_template,
    generate_labels,
    read_csv_data,
    validate_columns,
)

__version__ = "0.1.0"

__all__ = [
    "TEMPLATES",
    "detect_template",
    "generate_labels",
    "read_csv_data",
    "validate_columns",
]
