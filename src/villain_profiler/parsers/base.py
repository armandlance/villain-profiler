from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from ..models import Hand


class BaseParser(ABC):
    """Contrat commun : un parseur transforme du texte brut en objets Hand."""

    site: str = ""

    @abstractmethod
    def parse_text(self, text: str) -> list[Hand]: ...

    def parse_file(self, path: str | Path) -> list[Hand]:
        return self.parse_text(Path(path).read_text(encoding="utf-8", errors="replace"))
