from __future__ import annotations

from collections import defaultdict

from ..models import Hand


def group_by_game(hands: list[Hand]) -> dict[str, list[Hand]]:
    """Regroupe les mains par game_id (ordre d'apparition conservé).

    Les sites sans notion de game_id (ex. PokerStars ici) tombent dans le groupe "all".
    """
    groups: dict[str, list[Hand]] = defaultdict(list)
    for hand in hands:
        groups[hand.game_id or "all"].append(hand)
    return dict(groups)
