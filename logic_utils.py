def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    """Parse user input into an int guess."""
    if not raw or raw == "":
        return False, None, "Enter a guess."
    try:
        value = int(float(raw))
        return True, value, None
    except ValueError:
        return False, None, "That is not a number."


def check_guess(guess, secret):
    """Compare guess to secret and return (outcome, message)."""
    if guess == secret:
        return "Win", "🎉 Correct!"
    elif guess > secret:
        return "Too High", "📉 Go LOWER!"  # Fixed: Inversion corrected
    else:
        return "Too Low", "📈 Go HIGHER!"  # Fixed: Inversion corrected


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = max(10, 100 - 10 * (attempt_number + 1))
        return current_score + points
    if outcome == "Too High" or outcome == "Too Low":
        
        return current_score - 5 if outcome == "Too Low" else current_score + 5
    return current_score
