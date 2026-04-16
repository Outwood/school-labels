"""Initial password labels template for Avery 7160."""

from typing import override

from .email_password import EmailPasswordTemplate


class InitialPasswordTemplate(EmailPasswordTemplate):
    """Initial password labels template.

    Identical to email-password but labels the credential field 'Initial password'.
    """

    CREDENTIAL_LABEL: str = "Initial password"

    @property
    @override
    def name(self) -> str:
        return "initial-password"

    @property
    @override
    def pdf_title(self) -> str:
        return "Initial account stickers"
