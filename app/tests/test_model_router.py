import pytest
from app.heuristic_router import heuristic_tier

@pytest.mark.parametrize("query, expected", [
    # Empty input goes to the stronger model
    ("", "expert"),
    ("   ", "expert"),
    # Signal 1: comparison / correlation words
    ("compare smoking rates in Auckland", "expert"),
    ("COMPARE smoking rates in Auckland", "expert"),
    ("smokers vs non smokers in Otago", "expert"),
    ("relationship between income and tenure", "expert"),
    # Signal 2: two or more "and"s
    ("smokers in Auckland and Otago and Canterbury", "expert"),
    ("smokers in Auckland and Otago", "faster"),
    # "and" inside a word (Auckland) is not a conjunction
    ("smokers in Auckland, Rotorua", "faster"),
    # Signal 3: more than 25 words
    (" ".join(["smokers"] * 26), "expert"),
    (" ".join(["smokers"] * 25), "faster"),
    # Signal 4: several questions or sentences
    ("How many smokers? Where?", "expert"),
    ("number of smokers in Otago", "faster"),
    # Signal 5 and default: simple lookups
    ("How many smokers in Otago", "faster"),
    ("smokers in Otago", "faster"),
])

def test_heuristic_tier(query, expected):
    assert heuristic_tier(query) == expected