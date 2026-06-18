# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  When I first ran the app, the UI seemed to be functional on the surface, but the core gameplay was brokena nd unpredictable. The game felt impossible to play because it gave me wrong feedback and crashed.

  Two bugs that stood out to me:
  * **The New Game Crash:** Tapping the "Start New Game" button immediately threw a file system error and broke the session instead of resetting everything.
  * **Backwards Hints:** The high/low logic was completely inverted; guessing a number higher than the secret told me to go higher, and guessing lower told me to go lower.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Clicking on "Start New Game"| The game starts, attempts restart, and chooses a secret number| The game crashes and fails to restart| No such file exists|
| Guessing 94| "Go LOWER'"| "Go HIGHER"| Inverted error|
| Guessing 15| "Go HIGHER"| "Go LOWER"| Inverted error|

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Gemini and VS Code's integrated AI assistant as my programming partners for this project. A great example of the AI helping out was when it pinpointed a tricky type-coercion flaw, showing me that the secret number was being converted into a string on alternating turns and breaking normal integer comparisons. I verified it by checking the terminal outputs and watching the `TypeError` messages vanish once we forced both values to strictly remain integers. On the flip side, the AI completely sent me down a rabbit hole early on when it tried to fix my test file pathway failures by completely rewriting my source code logic. I caught the mistake by looking closely at the terminal stack trace, realizing it was just a local module resolution issue, and fixed it myself using `python -m pytest` instead of altering any application code.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

To make sure a bug was actually dead and gone, I paired manual testing in the browser with automated terminal runs. For instance, I ran `python -m pytest` in the terminal to trigger the test suite inside the `tests/` folder. Seeing all seven unit tests come back fully green proved that my refactored math logic inside `logic_utils.py` was holding up perfectly across all edge cases. The AI was super helpful here because it helped me break down exactly what the pre-written unit tests were looking for, making it easy to understand the expected parameters for scores and dynamic difficulty limits without having to guess.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

The easiest way to explain Streamlit to a friend is to imagine it like a flipbook that completely redraws the entire page from top to bottom every single time you interact with it—like clicking a button or moving a slider. Because it runs the script over and over from scratch, standard Python variables completely wipe out and reset every single time you click anything. Session state is basically like putting a sticky note on the back of that flipbook; it allows the app to remember data (like your current score or total attempts) across those constant page redraws so you don't lose your progress.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

Moving forward, I'm definitely going to keep up the habit of running tests via `python -m pytest` and keeping my logic separated into clean modules like `logic_utils.py` to enforce a solid separation of concerns. Next time I work with AI, I plan to ask it for targeted code traces to explain errors rather than letting it suggest massive, sweeping code overrides that clutter the architecture. This project really changed how I think about AI-generated code; it proved to me that even if an AI gives you a visually stunning, polished UI, the underlying math can still be full of hidden traps that require a human developer to audit and fix.
