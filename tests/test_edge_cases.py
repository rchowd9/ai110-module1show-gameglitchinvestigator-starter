"""Edge-case regression suite for the Game Glitch Investigator.

These tests probe three inputs that can still break the game even after the
"Go HIGHER/LOWER" and "New Game" glitches were fixed. Each test asserts the
*graceful* contract — the function should return a sane value, never raise an
unhandled exception or silently mislead the player.

Status against the current logic_utils.py (verified by running the code):

  Edge 1  check_guess(int, str)  -> raises TypeError   (FAILS until fixed)
  Edge 2  parse_guess("inf")     -> raises OverflowError (FAILS until fixed)
  Edge 3  parse_guess("50.9")    -> silently returns 50  (FAILS until fixed)

The whitespace / empty / "nan" cases already pass and lock in good behavior.
"""

import pytest

from logic_utils import check_guess, parse_guess


VALID_OUTCOMES = {"Win", "Too High", "Too Low"}


# ---------------------------------------------------------------------------
# Edge case 1: type-mismatched arguments to check_guess.
#
# app.py feeds a *string* secret to check_guess on even-numbered attempts
# (app.py:161-166), but logic_utils.check_guess compares with `>` and has no
# TypeError fallback. int-vs-str (and None-vs-int) comparison raises in Py3,
# crashing mid-game. Graceful contract: return a valid (outcome, message)
# tuple without raising.
# ---------------------------------------------------------------------------

def test_check_guess_string_secret_does_not_raise():
    # Equivalent values, one as str: must not crash, must report a win.
    outcome, message = check_guess(50, "50")
    assert outcome == "Win"
    assert isinstance(message, str) and message


@pytest.mark.parametrize(
    "guess, secret",
    [
        (60, "50"),   # guess higher than a string secret
        (40, "50"),   # guess lower than a string secret
        ("50", 50),   # roles reversed: string guess, int secret
    ],
)
def test_check_guess_mixed_types_returns_valid_outcome(guess, secret):
    outcome, message = check_guess(guess, secret)
    assert outcome in VALID_OUTCOMES
    assert isinstance(message, str) and message


def test_check_guess_none_guess_does_not_crash():
    # A missing/None guess should degrade gracefully, not raise TypeError.
    outcome, message = check_guess(None, 50)
    assert outcome in VALID_OUTCOMES
    assert isinstance(message, str) and message


# ---------------------------------------------------------------------------
# Edge case 2: non-finite and overflowing numeric strings to parse_guess.
#
# parse_guess does int(float(raw)) but only catches ValueError. "inf",
# "Infinity" and huge magnitudes like "1e999" overflow to float infinity,
# and int(inf) raises OverflowError -- which escapes uncaught and crashes the
# submit handler. Graceful contract: reject as a non-number.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "raw",
    ["inf", "-inf", "Infinity", "1e999", "-1e999", "1e400"],
)
def test_parse_guess_rejects_non_finite_input(raw):
    ok, value, err = parse_guess(raw)
    assert ok is False
    assert value is None
    assert isinstance(err, str) and err


def test_parse_guess_rejects_nan():
    # "nan" already parses gracefully today (int(nan) -> ValueError, caught).
    # Locked in so a future refactor can't regress it into a crash.
    ok, value, err = parse_guess("nan")
    assert ok is False
    assert value is None
    assert isinstance(err, str) and err


# ---------------------------------------------------------------------------
# Edge case 3: non-integer decimal strings to parse_guess.
#
# parse_guess silently truncates "50.9" -> 50 via int(float(...)). A player
# who types 50.9 against a secret of 50 is handed a *false win*; against 51,
# misleading feedback. Graceful contract: reject non-integer input so the
# player gets an honest "enter a whole number" style message instead of a
# silently altered guess.
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("raw", ["50.9", "0.5", "49.99", "-3.7"])
def test_parse_guess_rejects_non_integer_decimals(raw):
    ok, value, err = parse_guess(raw)
    assert ok is False, f"{raw!r} was silently truncated to {value!r}"
    assert value is None
    assert isinstance(err, str) and err


def test_parse_guess_accepts_clean_integer_with_whitespace():
    # Surrounding whitespace should still parse cleanly (already graceful).
    ok, value, err = parse_guess("  42  ")
    assert ok is True
    assert value == 42
    assert err is None


@pytest.mark.parametrize("raw", ["", "   ", "abc", "12abc", "0x1A"])
def test_parse_guess_rejects_blank_and_garbage(raw):
    ok, value, err = parse_guess(raw)
    assert ok is False
    assert value is None
    assert isinstance(err, str) and err
