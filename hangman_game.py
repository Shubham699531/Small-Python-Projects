import requests
import random
import string

# |  |    /\    |\  |   ___     |\  /|    /\    |\  |
# |--|   /--\   | \ |  |  ___   | \/ |   /__\   | \ |
# |  |  /    \  |  \|  |___| |  |    |  /    \  |  \|

# Getting list of words from this url using requests library
words = list(requests.get('https://www.randomlists.com/data/words.json').json()['data'])

# Remove words containing underscore or spaces
[words.remove(word) for word in words if (" " in word) or ("_" in word)]

# Standard ascii lower case characters
standard_ascii_characters = list(string.ascii_lowercase)
# Press any key to play the game, or 'q' to quit
while input('Press any key to continue. q to quit.').lower() !='q':
    random_word = str(random.choice(words))
    # Creating a set for chosen word
    random_word_set = set(random_word)
    # Printing number of letters in randomly chosen word
    print(f'Your word has {len(random_word)} letters.')
    # Making a set for storing user inputs
    user_entered_letters_set = set()
    # Let initial given chances be 6
    chances = 6
    # Running loop till chances left > 0 and length of set >0
    while len(random_word_set)>0 and chances>0:
        user_entered_letter = input('Enter your guessed letter \n').lower()
        # Validating the user input by checking if it's not already enetered and  
        # it is present in standard ascii lower case characters list
        if (user_entered_letter not in user_entered_letters_set) and (user_entered_letter in standard_ascii_characters):
            user_entered_letters_set.add(user_entered_letter)
            if user_entered_letter in random_word_set:
                # Removing user entered letter if it matches with random word's letter
                random_word_set.remove(user_entered_letter)
            else:
                # If user entered letter doesn't match, 1 chance is reduced
                chances -=1
        elif user_entered_letter in user_entered_letters_set:
            # If user enters already entered letter, he is notified with a print statement
            print(f'You already have entered {user_entered_letter}')
        else:
            # In all other cases, some unusual response message is printed
            print('You have entered something unusual. Please try again.')
        print(f'Chances left: {chances}')
        print(f'Your entered letters: {" ".join(user_entered_letters_set)}')
        current_word = [c if c in user_entered_letters_set else '_' for c in random_word]
        print(' '.join(current_word))
        # Printing lost and win messages
    if chances==0:
        print(f'You lost. The word was {random_word}')
    else:
        print('Congrats, You won!')