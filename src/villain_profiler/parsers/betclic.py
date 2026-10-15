from __future__ import annotations

import re

from ..models import Action, ActionType, Hand, Street
from .base import BaseParser

_HAND_SPLIT = re.compile(r"(?=^\*{3} HEADER \*{3}\s*$)", re.MULTILINE)

_GAME_ID = re.compile(r"^Game ID:\s*(\S+)", re.MULTILINE)
_HAND_ID = re.compile(r"^Hand ID:\s*(\S+)", re.MULTILINE)
_STAKES = re.compile(r"^Blinds:\s*([\d.,]+\s*/\s*[\d.,]+)", re.MULTILINE)
_PLAYER = re.compile(r"^Seat \d+:\s*(.+?)\s+\((\d+)\)\s*(?:\[(.*?)\])?\s*$")
_DEALT = re.compile(r"^(.+?):\s*\[([2-9TJQKA][cdhs])\s+([2-9TJQKA][cdhs])\]\s*$")
# Couvre aussi "Raises to 300 and is all-in" : la fin de ligne est ignorée.
_ACTION = re.compile(
    r"^\d{2}:\d{2}:\d{2}\s+-\s+(.+?):\s+"
    r"(Posts SB|Posts BB|Folds|Checks|Calls|Bets|Raises to)\b\s*([\d.,]*)"
)

_ACTION_TYPES = {
    "Folds": ActionType.FOLD,
    "Checks": ActionType.CHECK,
    "Calls": ActionType.CALL,
    "Bets": ActionType.BET,
    "Raises to": ActionType.RAISE,
}
# Les blindes sont forcées : ce ne sont pas des actions volontaires (VPIP/PFR).
_BLIND_POSTS = {"Posts SB", "Posts BB"}


class BetclicParser(BaseParser):
    site = "betclic"

    def parse_text(self, text: str) -> list[Hand]:
        hands: list[Hand] = []
        for chunk in _HAND_SPLIT.split(text):
            chunk = chunk.strip()
            if chunk.startswith("*** HEADER ***"):
                hand = self._parse_hand(chunk)
                if hand is not None:
                    hands.append(hand)
        return hands

    def _parse_hand(self, chunk: str) -> Hand | None:
        game_id_match = _GAME_ID.search(chunk)
        hand_id_match = _HAND_ID.search(chunk)
        if not game_id_match or not hand_id_match:
            return None

        stakes_match = _STAKES.search(chunk)
        hand = Hand(
            hand_id=hand_id_match.group(1),
            game_id=game_id_match.group(1),
            site=self.site,
            players=[],
            stakes=stakes_match.group(1).replace(" ", "") if stakes_match else "",
        )

        street: Street | None = None
        for line in chunk.splitlines():
            line = line.strip()

            if line == "*** HOLE CARDS ***":
                street = Street.PREFLOP
                continue
            if line.startswith("*** FLOP ***"):
                street = Street.FLOP
                continue
            if line.startswith("*** TURN ***"):
                street = Street.TURN
                continue
            if line.startswith("*** RIVER ***"):
                street = Street.RIVER
                continue
            if line.startswith("*** SHOWDOWN ***") or line.startswith("*** SUMMARY ***"):
                break

            if line.startswith("Seat "):
                match = _PLAYER.match(line)
                if match:
                    player_name, _stack, position = match.groups()
                    hand.players.append(player_name)
                    if position and "Hero" in position:
                        hand.hero = player_name
                continue

            if street is None:
                continue

            dealt = _DEALT.match(line)
            if dealt:
                hand.hero = dealt.group(1)
                hand.hero_cards = f"{dealt.group(2)} {dealt.group(3)}"
                continue

            action = _ACTION.match(line)
            if action:
                player, action_name, amount_text = action.groups()
                if action_name in _BLIND_POSTS:
                    continue
                amount = float(amount_text.replace(",", "")) if amount_text else 0.0
                hand.actions.append(Action(player, street, _ACTION_TYPES[action_name], amount))

        return hand
