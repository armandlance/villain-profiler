"""Classification V1 par règles. Seuils indicatifs pour du cash 6-max, à affiner."""
from __future__ import annotations

from dataclasses import dataclass

from ..stats import PlayerStats

FULL_CONFIDENCE_HANDS = 200


@dataclass(frozen=True)
class Profile:
    label: str
    confidence: float  # 0.0 à 1.0, selon la taille de l'échantillon


def classify(stats: PlayerStats, min_hands: int = 30) -> Profile:
    confidence = min(1.0, stats.hands / FULL_CONFIDENCE_HANDS)
    if stats.hands < min_hands:
        return Profile("Unknown", confidence)

    vpip, pfr = stats.vpip, stats.pfr
    if vpip < 13:
        label = "Nit"
    elif vpip >= 40 and pfr >= 25:
        label = "Maniac"
    elif vpip >= 28 and pfr >= 20:
        label = "LAG"
    elif vpip >= 28 and pfr < 15:
        label = "Calling Station"
    elif vpip <= 27 and pfr >= 0.6 * vpip:
        label = "TAG"
    else:
        label = "Weak-Tight"
    return Profile(label, confidence)
