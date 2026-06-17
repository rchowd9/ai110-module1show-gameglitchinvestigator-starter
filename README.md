# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

### Game Purpose
The app is a basic number-guessing game that sets an inclusive range of numbers based on the user's difficulty choice ("Easy", "Normal", or "Hard"). It manages state to track attempt history and updates player scores while providing helpful "Go HIGHER!" or "Go LOWER!" hints.


### Bugs found
I found three bugs that broke the game loop:
1. **The Inverted Hint Bug:** A messy type-coercion flaw forced the secret number into a string on every other turn. This threw a TypeError and kicked things down to a fallback block, which accidentally compared the values as text, resulting in completely backwards hints.

2. **The Hardcoded Reset Bug:** Hitting "New Game" completely ignored your chosen difficulty because the generation limits were hardcoded to 1-100 directly inside the UI code.

3. **The Score Multiplier Flaw:** The scoring function randomly padded your points with extra credit on alternating even attempts instead of cleanly penalizing wrong guesses.


### Fixes applied
1. **Refactored Architecture:** Cleaned up the codebase by moving all the core game logic out of app.py and into logic_utils.py.

2. **Fixed Type Rules & Labels:** Got rid of the alternating string mutation so the app strictly compares native integers, and flipped the return labels in check_guess so high guesses correctly tell you to go lower.

3. **Dynamic Difficulty Scaling:** Fixed the game reset loop to call `get_range_for_difficulty(difficulty)`, binding the number generation limits directly to whichever difficulty mode is active.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. **Select Difficulty:** The player chooses "Easy" mode in the sidebar, which sets an inclusive range of 1 to 20.
2.  **First Guess:** The user enters a guess of 15. The game calculates that the secret number is lower and returns "Go LOWER!"
3.  **Second Guess:** The user enters a guess of 5. The game calculates that the secret number is higher and returns "Go HIGHER!".
4.  **Score Updates:** The score and attempt counter update correctly after each submission.
5.  **Game Ends:** The user enters the correct guess of 10. The game registers the exact integer match, triggers the win screen, and the match ends.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

```
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\Home\Downloads\Game-Glitch\ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.13.0
collected 7 items                                                              

tests\test_game_logic.py .......                                         [100%]

============================== 7 passed in 0.16s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
