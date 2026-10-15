"""Calcul des statistiques préflop par joueur."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from ..models import ActionType, Hand, Street


@dataclass
class PlayerStats:
    name: str
    hands: int = 0
    vpip_count: int = 0
    pfr_count: int = 0
    three_bet_opps: int = 0
    three_bet_count: int = 0

    @staticmethod
    def _pct(num: int, den: int) -> float:
        return 100.0 * num / den if den else 0.0

    @property
    def vpip(self) -> float:
        return self._pct(self.vpip_count, self.hands)

    @property
    def pfr(self) -> float:
        return self._pct(self.pfr_count, self.hands)

    @property
    def three_bet(self) -> float:
        return self._pct(self.three_bet_count, self.three_bet_opps)


def compute_stats(hands: list[Hand]) -> dict[str, PlayerStats]:
    stats: dict[str, PlayerStats] = defaultdict(lambda: PlayerStats(name=""))

    for hand in hands:
        for p in hand.players:
            s = stats[p]
            s.name = p
            s.hands += 1

        vpip: set[str] = set()
        pfr: set[str] = set()
        opp_3bet: set[str] = set()
        did_3bet: set[str] = set()
        raises = 0

        for a in hand.actions_on(Street.PREFLOP):
            # 3-bet : le joueur fait face à exactement un raise avant lui
            if raises == 1 and a.player not in opp_3bet:
                opp_3bet.add(a.player)
                if a.type == ActionType.RAISE:
                    did_3bet.add(a.player)
            if a.type in (ActionType.CALL, ActionType.BET, ActionType.RAISE):
                vpip.add(a.player)
            if a.type == ActionType.RAISE:
                pfr.add(a.player)
                raises += 1

        for p in vpip:
            stats[p].vpip_count += 1
        for p in pfr:
            stats[p].pfr_count += 1
        for p in opp_3bet:
            stats[p].three_bet_opps += 1
        for p in did_3bet:
            stats[p].three_bet_count += 1

    return dict(stats)
