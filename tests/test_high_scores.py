"""Tests for the High Score tracker feature in logic_utils.

Covers the three things that matter for a persisted high-score system:
  * the record-beating logic is correct and non-destructive,
  * scores round-trip through a real file unchanged,
  * a missing or corrupt file never crashes the game.
"""

import json

import pytest

from logic_utils import (
    is_new_high_score,
    update_high_scores,
    load_high_scores,
    save_high_scores,
)


# ---------------------------------------------------------------------------
# Record-beating logic (pure, no I/O)
# ---------------------------------------------------------------------------

def test_first_score_for_difficulty_is_a_record():
    assert is_new_high_score({}, "Easy", 50) is True


def test_higher_score_beats_existing():
    assert is_new_high_score({"Easy": 50}, "Easy", 80) is True


def test_lower_or_equal_score_is_not_a_record():
    assert is_new_high_score({"Easy": 80}, "Easy", 80) is False
    assert is_new_high_score({"Easy": 80}, "Easy", 30) is False


def test_negative_score_can_still_be_a_first_record():
    # update_score can go negative; the first such run should still register.
    assert is_new_high_score({}, "Hard", -15) is True


def test_update_returns_record_flag_and_does_not_mutate_input():
    original = {"Easy": 50}
    updated, is_record = update_high_scores(original, "Easy", 90)
    assert is_record is True
    assert updated == {"Easy": 90}
    # The caller's dict must be left untouched.
    assert original == {"Easy": 50}


def test_update_keeps_better_existing_score():
    updated, is_record = update_high_scores({"Easy": 90}, "Easy", 40)
    assert is_record is False
    assert updated == {"Easy": 90}


def test_update_tracks_each_difficulty_independently():
    scores = {}
    scores, _ = update_high_scores(scores, "Easy", 30)
    scores, _ = update_high_scores(scores, "Hard", 70)
    assert scores == {"Easy": 30, "Hard": 70}


# ---------------------------------------------------------------------------
# Persistence round-trip
# ---------------------------------------------------------------------------

def test_save_then_load_round_trips(tmp_path):
    path = tmp_path / "high_scores.json"
    scores = {"Easy": 95, "Normal": 80, "Hard": 70}
    save_high_scores(scores, path=str(path))
    assert load_high_scores(path=str(path)) == scores


def test_save_overwrites_previous_file(tmp_path):
    path = tmp_path / "high_scores.json"
    save_high_scores({"Easy": 10}, path=str(path))
    save_high_scores({"Easy": 99}, path=str(path))
    assert load_high_scores(path=str(path)) == {"Easy": 99}


# ---------------------------------------------------------------------------
# Graceful degradation
# ---------------------------------------------------------------------------

def test_load_missing_file_returns_empty(tmp_path):
    path = tmp_path / "does_not_exist.json"
    assert load_high_scores(path=str(path)) == {}


def test_load_corrupt_json_returns_empty(tmp_path):
    path = tmp_path / "high_scores.json"
    path.write_text("{not valid json", encoding="utf-8")
    assert load_high_scores(path=str(path)) == {}


def test_load_non_dict_json_returns_empty(tmp_path):
    path = tmp_path / "high_scores.json"
    path.write_text("[1, 2, 3]", encoding="utf-8")
    assert load_high_scores(path=str(path)) == {}


def test_load_drops_malformed_entries_but_keeps_valid_ones(tmp_path):
    path = tmp_path / "high_scores.json"
    # Mix of good and bad rows: bools, strings, and floats must be discarded.
    path.write_text(
        json.dumps({"Easy": 50, "Normal": "oops", "Hard": True, "Wild": 12.5}),
        encoding="utf-8",
    )
    assert load_high_scores(path=str(path)) == {"Easy": 50}
