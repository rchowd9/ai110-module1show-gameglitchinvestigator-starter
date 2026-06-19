# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

* Challenge 1: Advanced Edge-Case Testing
* Challenge 2: Feature Expansion

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

I tasked the agent with planning and implementing a brand-new "High Score" tracker stretch feature. The requirements were that it had to dynamically track best scores per difficulty level, persist the data locally across game reboots, handle missing or corrupted files gracefully, and include a full suite of automated unit tests to match our existing robust testing architecture.

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

The agent executed a multi-step implementation across three primary files:

1. **`logic_utils.py`**: Appended pure, testable helper functions (`load_high_scores`, `is_new_high_score`, `update_high_scores`, and `save_high_scores`) to manage an atomic JSON save file system (using a temporary file + `os.replace` to prevent file corruption if the game is suddenly interrupted).

2. **`app.py`**: Wired the backend helpers into the UI layer. It added a clean 🏆 sidebar panel that dynamically displays records alongside a 👑 icon highlighting the current difficulty setting. It also added a check at the end of a match to trigger a celebration banner whenever a new record is smashed.

3. **`tests/test_high_scores.py`**: Created a brand-new testing suite containing 13 independent test cases checking file round-trips, record-breaking calculations, negative scores, and file resilience when loading corrupted or poorly formatted JSON.

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

I reviewed the agent's work and verified that it correctly imported code cleanly from `logic_utils.py` without code duplication or disturbing the pre-existing logic loops. I ran the full automated suite via `python -m pytest tests/` to confirm that all 42 tests passed perfectly and verified that `app.py` compiled cleanly. A couple of specific architectural design choices were confirmed during review:

* High scores are tracked dynamically across both wins and losses since a long, intense losing run can still mathematically rack up a competitive point total under the scoring rules.

* The application automatically generates a local `high_scores.json` file in the project folder upon saving its very first high score.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| **Type-Mismatched Arguments**| Identify three potential edge case inputs that might still break the game and then generate a suite of pytest cases that verify the game handles these inputs gracefully.| test_check_guess_string_secret_does_not_raise| Yes it passed| `app.py` passes the secret as a string on even turns, which breaks the logic and crashes the game unless the utility function strictly handles the type cast.|
| **Non-Finite / Overflowing Strings**| Identify three potential edge case inputs that might still break the game and then generate a suite of pytest cases that verify the game handles these inputs gracefully.| `test_parse_guess_rejects_non_finite_input`| Yes it passed| If a user inputs infinity (`inf` or `1e999`), it bypasses regular number validation and throws an unhandled `OverflowError` right into the user's face.|
| **Non-Integer Decimals**| Identify three potential edge case inputs that might still break the game and then generate a suite of pytest cases that verify the game handles these inputs gracefully.| test_parse_guess_rejects_non_integer_decimals`| Yes it passed| Typing a decimal like `50.9` would get silently chopped down to `50` by `int()`, giving players a confusing experience or a cheap, unearned win.|

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
