- Understand the purpose of http methods/verbs.
- Understand the separation of views/endpoints and internal models and logic.
- Understand why task queues or out-of-sequence running of code is important.
- Understand status codes? This might be irrelevant for endpoints thanks to
intuitive endpoints exceptions.

What were some of the trade-offs or struggles you faced when implementing the new game logic?

Orginaly i was going to have the user provide the word they wanted to guess, similar to how the guessing game worked. But later i decided that it might be better to also provide a list of valid words as part of the game it self.

Model wise Hangman is very similar to the guessing game. The differnce is isntead guessing a word instead fo a number. I had to add a some extra string to visually show the the word in a ***A*** format, so that the user could see where the letter was and better guess what the other letters could be 