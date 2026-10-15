from pathlib import Path

from villain_profiler.parsers.betclic import BetclicParser
from villain_profiler.stats import compute_stats, group_by_game

SAMPLE = Path(__file__).parent.parent / "data/samples/betclic_sample.txt"


def load_hands():
    return BetclicParser().parse_text(SAMPLE.read_text(encoding="utf-8"))


def test_betclic_txt():
    mains = load_hands()

    assert len(mains) == 48
    assert mains[0].game_id == "01M4Y6GRE8X1Y3H5Y3FRJ52CAT"
    assert mains[0].hand_id == "01M4Y6VK3NF27CWDEAJMJVDGQA"
    assert mains[0].hero == "Sitsou"
    assert mains[0].hero_cards == "2s Td"


def test_blinds_are_not_voluntary_actions():
    # 2e main : Sitsou (SB) fold, l'adversaire (BB) gagne sans agir.
    # Aucune des deux blindes ne doit compter comme VPIP.
    stats = compute_stats([load_hands()[1]])
    assert all(s.vpip_count == 0 for s in stats.values())


def test_group_by_game():
    hands = load_hands()
    games = group_by_game(hands)
    assert len(games) == 2
    assert sum(len(h) for h in games.values()) == 48
    assert all(h.game_id == gid for gid, hs in games.items() for h in hs)
