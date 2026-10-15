from .base import BaseParser
from .betclic import BetclicParser
from .pokerstars import PokerStarsParser
from .winamax import WinamaxParser

PARSERS: dict[str, type[BaseParser]] = {
    "pokerstars": PokerStarsParser,
    "winamax": WinamaxParser,
    "betclic": BetclicParser,
}


def get_parser(site: str) -> BaseParser:
    try:
        return PARSERS[site.lower()]()
    except KeyError:
        raise ValueError(f"Site non supporté: {site}. Disponibles: {', '.join(PARSERS)}")


__all__ = ["BaseParser", "get_parser", "PARSERS"]
