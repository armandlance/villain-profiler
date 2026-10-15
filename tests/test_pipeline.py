from pathlib import Path

from villain_profiler.parsers import get_parser
from villain_profiler.profiling import classify
from villain_profiler.stats import compute_stats

SAMPLE = Path(__file__).parent.parent / "data/samples/pokerstars_sample.txt"


def test_parse_sample():
    hands = get_parser("pokerstars").parse_file(SAMPLE)
    assert len(hands) == 3
    assert hands[0].players == ["Alice", "Bob", "Carol"]
    assert hands[0].hero == "Carol"


def test_stats():
    stats = compute_stats(get_parser("pokerstars").parse_file(SAMPLE))
    alice, carol = stats["Alice"], stats["Carol"]
    assert alice.hands == 3 and alice.vpip_count == 1 and alice.pfr_count == 1
    assert carol.three_bet_opps == 1 and carol.three_bet_count == 1


def test_unknown_when_small_sample():
    stats = compute_stats(get_parser("pokerstars").parse_file(SAMPLE))
    assert classify(stats["Alice"]).label == "Unknown"
