"""school-labels - PDF label generation tool for schools."""

from .generator import (
    TEMPLATES,
    detect_template,
    generate_labels,
    validate_columns,
)

__all__ = [
    "TEMPLATES",
    "detect_template",
    "generate_labels",
    "validate_columns",
]
