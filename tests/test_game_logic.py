from logic_utils import check_guess, get_range_for_difficulty


# ---------------------------------------------------------------------------
# "Go HIGHER / Go LOWER" bug
#
# check_guess returns a (outcome, message) tuple. The original glitch was that
# the *message* was inverted relative to the *outcome*: a guess that was too
# high told the player to "Go HIGHER". So it is not enough to check the outcome
# label — we must also assert the direction of the hint text.
# ---------------------------------------------------------------------------

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_too_high_outcome_and_message():
    # Guess (60) is above the secret (50): outcome is "Too High"...
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    # ...and the hint must point DOWN. This is the bug that was reported.
    assert "LOWER" in message.upper()
    assert "HIGHER" not in message.upper()


def test_too_low_outcome_and_message():
    # Guess (40) is below the secret (50): outcome is "Too Low"...
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    # ...and the hint must point UP.
    assert "HIGHER" in message.upper()
    # "HIGHER" contains no "LOWER", so this guards against re-inversion.
    assert "GO LOWER" not in message.upper()


# ---------------------------------------------------------------------------
# "New Game" bug
#
# The New Game handler in app.py hardcoded random.randint(1, 100) instead of
# using the difficulty range. The testable root cause is get_range_for_difficulty:
# a new game must draw its secret from the range matching the chosen difficulty.
# ---------------------------------------------------------------------------

def test_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)


def test_range_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)


def test_range_hard():
    # Before the fix a new Hard game still used 1-100; it must use 1-50.
    assert get_range_for_difficulty("Hard") == (1, 50)


def test_range_unknown_defaults_to_normal():
    assert get_range_for_difficulty("Impossible") == (1, 100)
