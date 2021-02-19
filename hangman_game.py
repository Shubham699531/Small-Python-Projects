import requests
import random

# |  |    /\    |\  |   ___     |\  /|    /\    |\  |
# |--|   /--\   | \ |  |  ___   | \/ |   /__\   | \ |
# |  |  /    \  |  \|  |___| |  |    |  /    \  |  \|

# Getting list of words from this url using requests library
words = list(requests.get('https://www.randomlists.com/data/words.json').json()['data'])

# Remove words containing underscore or spaces
[words.remove(word) for word in words if (" " in word) or ("_" in word)]

# Press any key to play the game, or 'q' to quit
while input('Press any button to play. q to quit\n').lower() != 'q':
    # Selecting a random word from list of words
    random_word = words[random.randint(0,len(words))]
    # Printing length of random word for user reference
    print(f'Length of your word is {len(random_word)}')
    # Initializing predicted word array with '_' for length of words
    # Ex: if it's a 3 letter word, predicted_word_array will be = ["_", "_", "_"]
    predicted_word_array = ["_"] * len(random_word)
    # Let initial given chances be 6
    chances_left = 6
    # Running loop till chances left > 0
    while chances_left>0:
        # keeping a flag for checking if guessed letter matches a letter in selected random word
        flag = True
        guessed_letter = input('Enter your guess: ')
        for i, w in enumerate(random_word):
            # If guessed letter matches random word's letter
            if guessed_letter == w:
                # Replacing "_" with guessed_letter
                predicted_word_array[i] = guessed_letter
                # Making flag false because a match is found
                flag = False
        # If flag is true, meaning guessed letter doesn't match random word's letter
        if flag:
            # Reduce number of chances by 1 and printing number of left chances
            chances_left -=1
            print(f'You have {chances_left} chances left.')
        print(predicted_word_array)
    # Printing 'You lost' message, since number of chances become 0
    print(f'You lost. The word was {random_word}')

