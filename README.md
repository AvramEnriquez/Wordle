# Wordle
A command line version of the game Wordle. Guess the word within six tries. Start running wordle_database.py to begin.

The game starts by importing the random module and the words list from the wordle_words module. It then converts all words to uppercase using the map() function.

Next, the code defines a color class that contains ANSI code modifiers for strings in the terminal.

The random_word() function selects a random word from the words list and returns it in uppercase format.

The wordle() function contains the actual game logic. It first selects a random word using the random_word() function and initializes variables to keep track of the user's guesses, number of tries, and whether the user has won. It also creates a keyboard string that displays the letters available for guessing.

The function then enters a loop that continues until the user wins or reaches six tries. In each iteration of the loop, the user enters a five-letter word guess, and the code checks if it is a valid guess. If the guess is invalid, the code prints an error message and asks the user to guess again. If the guess is valid, the code compares it to the actual word and displays the letters in the guess with different colors based on whether they are correct, incorrect, or partially correct. The keyboard string is also updated to highlight the letters that the user has guessed.

If the user correctly guesses the word, the loop ends, and the code displays a message indicating that the user has won. If the user reaches six tries without guessing the word, the loop ends, and the code displays a message indicating that the user has lost.

The wordle() function returns the number of tries, whether the user won, and a boolean value indicating whether the user's streak should be cleared in the database.


The most difficult part of writing this was figuring out the color coding logic for a correct character where:
- The number of characters in a guess > actual number of characters in wordle
- All character positions were guessed correctly (green)

Another challenge I faced when writing this code was creating a guess distribution bar chart that plotted from a base of 0
AKA Plot all guess distribution even if value is 0.
Eventually I figured out how to use a subsitution for loop and a base list of tuples to gain the desired plotted bar chart.


May not work on Windows

Words sourced from: https://github.com/tabatkins/wordle-list
