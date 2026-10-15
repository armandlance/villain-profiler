from __future__ import annotations

from ..models import Hand
from .base import BaseParser


class WinamaxParser(BaseParser):
    """TODO : implémenter le format Winamax (ajouter un exemple dans data/samples/)."""

    site = "winamax"

    def parse_text(self, text: str) -> list[Hand]:
        raise NotImplementedError("Le parseur Winamax n'est pas encore implémenté.")
