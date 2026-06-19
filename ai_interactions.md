# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

Challenge 1: Advanced Edge-Case Testing

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

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
