from __future__ import annotations

import argparse

from .advisor import advise
from .parsers import PARSERS, get_parser
from .profiling import classify
from .stats import compute_stats


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(prog="villain", description="Profilage d'adversaires au poker")
    sub = ap.add_subparsers(dest="cmd", required=True)
    an = sub.add_parser("analyze", help="Analyser un fichier de hand histories")
    an.add_argument("file")
    an.add_argument("--site", default="pokerstars", choices=list(PARSERS))
    an.add_argument("--min-hands", type=int, default=30)
    args = ap.parse_args(argv)

    hands = get_parser(args.site).parse_file(args.file)
    stats = compute_stats(hands)
    print(f"{len(hands)} mains analysées, {len(stats)} joueurs\n")
    print(f"{'Joueur':<14}{'Mains':>6}{'VPIP':>7}{'PFR':>7}{'3bet':>7}  {'Profil':<16}Conf.")
    for s in sorted(stats.values(), key=lambda x: -x.hands):
        p = classify(s, args.min_hands)
        print(f"{s.name:<14}{s.hands:>6}{s.vpip:>6.0f}%{s.pfr:>6.0f}%{s.three_bet:>6.0f}%  "
              f"{p.label:<16}{p.confidence:.0%}")
        for tip in advise(p.label):
            print(f"    - {tip}")


if __name__ == "__main__":
    main()
