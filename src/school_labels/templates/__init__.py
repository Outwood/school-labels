"""Label templates for different sheet types and layouts."""

from .avery7160 import Avery7160Template
from .base import LabelTemplate
from .email_password import EmailPasswordTemplate
from .initial_password import InitialPasswordTemplate

__all__ = [
    "Avery7160Template",
    "EmailPasswordTemplate",
    "InitialPasswordTemplate",
    "LabelTemplate",
]
