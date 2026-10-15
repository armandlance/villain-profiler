"""Modèle de données commun, indépendant du site de poker."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Street(str, Enum):
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"


class ActionType(str, Enum):
    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    BET = "bet"
    RAISE = "raise"


@dataclass(frozen=True)
class Action:
    player: str
    street: Street
    type: ActionType
    amount: float = 0.0


@dataclass
class Hand:
    hand_id: str
    site: str
    players: list[str]
    actions: list[Action] = field(default_factory=list)
    stakes: str = ""
    button_seat: int | None = None
    hero: str | None = None
    hero_cards: str | None = None
    game_id: str = ""  # identifiant de la partie/table (ex. un Spin Betclic)

    def actions_on(self, street: Street) -> list[Action]:
        return [a for a in self.actions if a.street == street]
