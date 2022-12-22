import random
from wordle_words import words
words = list(map(str.upper, words))

class color:
    """ANSI Code modifiers for strings in Terminal"""
    GREENBOX = '\x1b[6;30;42m'
    YELLOWBOX = '\x1b[6;30;43m'
    GRAYBOX = '\x1b[6;30;40m'
    GREENTEXT = '\033[92m'
    YELLOWTEXT = '\033[93m'
    BOLDTEXT = '\033[1m'
    END = '\033[0m' + '\x1b[0m'

def random_word(word_list):
    """Select random word to guess."""
    word = random.choice(word_list)
    return word.upper()

def wordle():
    """Actual Wordle game"""
    word = random_word(words)
    alphabet = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    tries = 0
    keyboard = "QWERTYUIOP\n ASDFGHJKL\n  ZXCVBNM"
    win = False

    while win == False:
        # End program if tries reaches 6
        if tries == 6:
            print(f'Sorry, you lost. The word was {word}')
            exit()

        # While loop for Input
        while True:
            user_word = input('Guess a 5-letter word: ').upper()
            if not all(char in alphabet for char in user_word):
                print("The following invalid character(s) were entered: {}"
                    .format(" ".join(set(user_word) - alphabet)))
            elif len(user_word) != 5:
                print("The guess must be 5 characters long.")
            elif user_word not in words:
                print("Invalid word, guess again.")
            else:
                break

        # For loop to adjust text color and keyboard highlights
        full_word = ''
        for user_char, word_char in zip(user_word, word):  # list(zip('abc', 'xyz')) = [('a', 'x'), ('b', 'y'), ('c', 'z')]
            if user_char == word_char:
                text = (color.BOLDTEXT + color.GREENTEXT + str(user_char) + color.END)
                keyboard = keyboard.replace(user_char, color.GREENBOX + user_char + color.END)
            elif user_char in word:
                text = (color.BOLDTEXT + color.YELLOWTEXT + str(user_char) + color.END)
                # If character on keyboard already green, do not turn yellow
                if (color.GREENBOX + user_char + color.END) in keyboard:
                    pass
                else:
                    keyboard = keyboard.replace(user_char, color.YELLOWBOX + user_char + color.END)
            else:
                text = (color.BOLDTEXT + str(user_char) + color.END)
                keyboard = keyboard.replace(user_char, color.GRAYBOX + user_char + color.END)
            
            full_word += text

            # If all of this character was guessed correctly (green) turn all other yellow characters gray        
            # If # of guesses > actual
            if (user_word.count(user_char) > word.count(user_char) and
                    # And if all correct positions have been found
                    full_word.count(color.GREENTEXT + str(user_char) + color.END) == word.count(user_char)):
                # Replace all yellow characters with gray
                full_word = full_word.replace(color.YELLOWTEXT + str(user_char) + color.END, str(user_char) + color.END)

        # If word guess is all green (correct), set win as True
        if full_word.count(color.GREENTEXT) == len(word):
            win = True

        print(full_word)
        print('')
        print(keyboard)
        print('')

        tries += 1
        print('Tries: ' + str(tries))
    
    print(f'You\'ve correctly guessed the word {word}. It took {tries} tries.')
    return tries, win
