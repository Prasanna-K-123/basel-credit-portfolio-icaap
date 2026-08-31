from __future__ import annotations

RANDOM_STATE = 20260831
N_OBLIGORS = 5000
N_SIMULATIONS = 100000
BASEL_MIN_PD = 0.0003
BASEL_CONFIDENCE = 0.999
MIN_CAPITAL_RATIO = 0.08

RATING_PDS = {
    "A": 0.0020,
    "BBB": 0.0050,
    "BB": 0.0150,
    "B": 0.0450,
    "CCC": 0.1200,
}

SECTORS = (
    "financials",
    "industrials",
    "consumer",
    "technology",
    "energy",
    "real_estate",
    "healthcare",
)

REGIONS = ("north", "south", "east", "west")
