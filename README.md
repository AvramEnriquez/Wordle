# Wordle
 Guess the word in 6 tries. Start running wordle_database.py to begin.
 
 This code makes use of ANSI escape code via Unix terminal to color code both a guess and keyboard output.

 The most difficult part of writing this was figuring out the color coding logic for a correct character where:
 - The number of characters in a guess > actual number of characters in wordle
 - All character positions were guessed correctly (green)

 Another challenge I faced when writing this code was creating a guess distribution bar chart that plotted from a base of 0
 AKA Plot all guess distribution even if value is 0.
 Eventually I figured out how to use a subsitution for loop and a base list of tuples to gain the desired plotted bar chart.


May not work on Windows

Words sourced from: https://github.com/tabatkins/wordle-list
