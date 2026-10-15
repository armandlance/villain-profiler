# villain-profiler

Analyse de hand histories de poker : calcul des stats (VPIP, PFR, 3-bet...), classification des profils adverses (Nit, TAG, LAG, Calling Station, Maniac...) et recommandations d'exploitation.

> **Outil de revue post-session uniquement.** Il n'est pas conçu pour une aide en temps réel pendant le jeu, ce qui est interdit par la plupart des sites.

## Installation

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Utilisation

```bash
villain analyze data/samples/pokerstars_sample.txt --site pokerstars --min-hands 3
```

## Pipeline

```
Hand histories -> parsers -> models -> stats -> profiling -> advisor
```

| Module | Rôle |
|---|---|
| `parsers/` | Un parseur par site, produit des objets `Hand` |
| `models/` | `Hand`, `Action`, `Street`, `ActionType` |
| `stats/` | VPIP, PFR, 3-bet par joueur |
| `profiling/` | Classification par règles + niveau de confiance |
| `advisor/` | Conseils d'exploitation par profil |

## Roadmap

- [x] Parseur PokerStars (cash, préflop)
- [x] VPIP / PFR / 3-bet
- [x] Profils par règles + confiance
- [ ] Parseur Winamax / GGPoker
- [ ] Stats postflop (c-bet, fold to c-bet, WTSD, AF)
- [ ] Fold to 3-bet, positions (BTN, CO, BB...)
- [ ] Clustering (K-Means / GMM)
- [ ] Calcul d'équité (eval7)
- [ ] Dashboard Streamlit

## Données

Ne committe jamais de vraies hand histories : `data/raw/` est ignoré par git. Anonymise les pseudos dans `data/samples/`.

## Licence

MIT
