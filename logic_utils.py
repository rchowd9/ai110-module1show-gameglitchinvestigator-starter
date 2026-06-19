import json
import math
import os

def get_range_for_difficulty(difficulty: str):
    """Return the (min_val, max_val) inclusive range based on chosen difficulty."""
    if difficulty == "Easy":
        return 1, 20
    elif difficulty == "Hard":
        return 1, 50
    else:  # Default to Normal
        return 1, 100

def parse_guess(raw: str):
    """Parse user input into an int guess while catching edge cases."""
    if not raw or raw.strip() == "":
        return False, None, "Enter a guess."
    
    try:
        val_float = float(raw)
        
        # Edge Case 2: Reject non-finite numbers like inf or Infinity
        if not math.isfinite(val_float):
            return False, None, "Please enter a valid finite number."
            
        # Edge Case 3: Explicitly reject non-integer decimals (like 50.9)
        if not val_float.is_integer():
            return False, None, "Please enter a whole number."
            
        return True, int(val_float), None
        
    except (ValueError, OverflowError):
        # Catches garbage text ("abc") or extreme numbers that overflow the float parser
        return False, None, "Please enter a valid number."


def check_guess(guess, secret):
    """Compare guess to secret and return (outcome, message)."""
    # Edge Case 1: Gracefully handle a completely missing/None guess
    if guess is None:
        return "Too Low", "Enter a valid guess."
        
    try:
        # Enforce that both inputs are integers to stop TypeErrors right here
        guess_int = int(guess)
        secret_int = int(secret)
    except (ValueError, TypeError):
        return "Too Low", "Invalid inputs."

    # Core game loop evaluations matching VALID_OUTCOMES
    if guess_int == secret_int:
        return "Win", "🎉 Correct!"
    elif guess_int > secret_int:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


# ---------------------------------------------------------------------------
# High Score tracker
#
# Best score is tracked per difficulty and persisted to a JSON file so it
# survives across sessions. Every read/write degrades gracefully: a missing or
# hand-mangled file is treated as "no scores yet" rather than crashing the game.
# ---------------------------------------------------------------------------

# Stored next to this module so it is found regardless of the working directory.
HIGH_SCORES_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "high_scores.json"
)


def load_high_scores(path: str = HIGH_SCORES_FILE):
    """Load per-difficulty best scores, e.g. {"Easy": 95, "Hard": 70}.

    A missing file, unreadable file, or corrupt/non-dict JSON yields an empty
    dict instead of raising. Only well-formed {str: int} entries are kept, so a
    partially mangled file still loads its valid rows.
    """
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (FileNotFoundError, OSError, ValueError):
        return {}

    if not isinstance(data, dict):
        return {}

    clean = {}
    for key, value in data.items():
        # bool is a subclass of int; exclude it so True/False can't pose as a score.
        if isinstance(key, str) and isinstance(value, int) and not isinstance(value, bool):
            clean[key] = value
    return clean


def is_new_high_score(scores: dict, difficulty: str, score: int) -> bool:
    """True if `score` beats the stored best for `difficulty` (or none exists)."""
    current = scores.get(difficulty)
    return current is None or score > current


def update_high_scores(scores: dict, difficulty: str, score: int):
    """Return (new_scores, is_record) without mutating the input dict.

    The score is recorded only when it is a new record, so a worse run never
    overwrites a better one.
    """
    record = is_new_high_score(scores, difficulty, score)
    updated = dict(scores)
    if record:
        updated[difficulty] = score
    return updated, record


def save_high_scores(scores: dict, path: str = HIGH_SCORES_FILE):
    """Atomically persist the high-score dict as JSON.

    Writes to a temp file then replaces the target, so an interrupted write
    can't leave a half-written (corrupt) high-score file behind.
    """
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(scores, fh, indent=2, sort_keys=True)
    os.replace(tmp, path)
    return scores