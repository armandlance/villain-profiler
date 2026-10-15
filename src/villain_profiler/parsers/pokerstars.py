from __future__ import annotations

import re

from ..models import Action, ActionType, Hand, Street
from .base import BaseParser

_HAND_SPLIT = re.compile(r"(?=^PokerStars (?:Zoom )?Hand #)", re.MULTILINE)
_HEADER = re.compile(r"Hand #(\d+):.*?\(([^)]*)\)")
_BUTTON = re.compile(r"Seat #(\d+) is the button")
_SEAT = re.compile(r"^Seat \d+: (.+?) \(")
_ACTION = re.compile(r"^(.+?): (folds|checks|calls|bets|raises)\b(?: \D*?([\d.,]+))?")
_DEALT = re.compile(r"^Dealt to (.+?) \[(.+?)\]")
_STREET_MARKERS = {
    "*** HOLE CARDS ***": Street.PREFLOP,
    "*** FLOP ***": Street.FLOP,
    "*** TURN ***": Street.TURN,
    "*** RIVER ***": Street.RIVER,
}
_ACTION_TYPES = {
    "folds": ActionType.FOLD,
    "checks": ActionType.CHECK,
    "calls": ActionType.CALL,
    "bets": ActionType.BET,
    "raises": ActionType.RAISE,
}


class PokerStarsParser(BaseParser):
    site = "pokerstars"

    def parse_text(self, text: str) -> list[Hand]:
        hands = []
        for chunk in _HAND_SPLIT.split(text):
            chunk = chunk.strip()
            if chunk.startswith("PokerStars"):
                hand = self._parse_hand(chunk)
                if hand:
                    hands.append(hand)
        return hands

    def _parse_hand(self, chunk: str) -> Hand | None:
        lines = chunk.splitlines()
        header = _HEADER.search(lines[0])
        if not header:
            return None
        hand = Hand(hand_id=header.group(1), site=self.site, players=[], stakes=header.group(2))

        street: Street | None = None
        for line in lines[1:]:
            if line.startswith("*** SHOW DOWN") or line.startswith("*** SUMMARY"):
                break
            marker = line.split(" [")[0]
            if marker in _STREET_MARKERS:
                street = _STREET_MARKERS[marker]
                continue
            if street is None:
                if m := _BUTTON.search(line):
                    hand.button_seat = int(m.group(1))
                elif m := _SEAT.match(line):
                    hand.players.append(m.group(1))
                continue
            if m := _DEALT.match(line):
                hand.hero, hand.hero_cards = m.group(1), m.group(2)
            elif m := _ACTION.match(line):
                amount = float(m.group(3).replace(",", "")) if m.group(3) else 0.0
                hand.actions.append(Action(m.group(1), street, _ACTION_TYPES[m.group(2)], amount))
        return hand
