# Wordle
 Guess the word in 6 tries
 
 This code makes use of ANSI escape code via Unix terminal to color code both a guess and keyboard output. May not work on Windows.

 The most difficult part of writing this was figuring out the color coding logic for a correct character where:
 - The number of characters in a guess > actual number of characters in wordle
 - All character positions were guessed correctly (green)

 Words sourced from: https://github.com/tabatkins/wordle-list