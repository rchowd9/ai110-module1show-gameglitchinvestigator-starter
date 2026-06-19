import math

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