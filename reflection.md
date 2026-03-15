# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").


When I first ran the game I noticed that you can't submit your guess by hitting the 'Enter' key (this isn't necessarily a bug, more of a preference find). Then while looking at the 'Developer Debug Info' I noticed the hint was providing the wrong direction (i.e. when user should be guessing higher numbers it recommends that they guess lower numbers). It was also unclear how the scoring data mattered since it wasn't shown to the user but only for the developer. Another visual bug I noted was that once you selected 'New Game' in theory all remnants of the last game should disappear, but the 'Game Over' notifiction remained at the bottom of the screen throughout the new game.


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

Used Claude Code to fix a few identified bugs. One of the bug fixes was the miscontrued difficulty ranges and the hardcoded range used for new games. First, I asked Claude to explain the logic behind the range issues and it brought to my attention the hardcoded range of 1 to 100 when a new game is commenced. I advised for it to correct the issue and it added the low and high variables that are pulled from the 'get_range_for_difficulty' function. What Claude didn't notice was that the Normal and Hard ranges were switched, and when I brought attention to the Hard range being smaller than Normal Claude advised increasing Hard to range 1 to 200 instead of swapping the number values. Although, I did accept the change since technically it works as long as the ranges increase along with the difficulty. Results were confirmed by mentally walking through the code, creating test cases for a few of the fixes, and then running the program itself.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed if it performed its base function accordingly. For the hardcoded range bug, I just needed to confirm that when the difficulty changed the range changed and didn't maintain the 1 to 100 values if not on Normal difficulty. AI was highly beneficial when creating the pytest cases. As I don't have much background creating pytests, Claude broke down each test case, created helpful comments to explain what the test was for and the result we would be looking for.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit "reruns" is basically a page or feature reload, while the session state is the current status of you site. You can think of session state as if you are writing a paper, the state maintains your writing but if you reset your state it is like starting on a new blank sheet of paper.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

