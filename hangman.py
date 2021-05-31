''' This program simulates a game of hangman. The computer will generate a word or phrase for the user to guess,
and the user will keep guessing letters until they either run out of guesses or guess the word correctly. 
Created by Stephanie Papa for the final project in Stanford's Code in Place 2021.'''

import random
import collections

# Sets specific sections from the word list the program can pull from to choose a word based off of difficulty.
RANDOM_MIN_EASY = 3
RANDOM_MAX_EASY = 78
RANDOM_MIN_MEDIUM = 82
RANDOM_MAX_MEDIUM = 165
RANDOM_MIN_HARD = 169
RANDOM_MAX_HARD = 319
# Global for base number of incorrect guesses and hints a player can have.
MAX_GUESSES = 8
MAX_HINTS = 1

def main():
    # Explains how the game works.
    starting_message()
    # Requests a difficulty level from the user and plays corresponding difficulty.
    difficulty_level()
    # Asks the user if they want to play again.
    play = play_again()
    # Repeats game play while user wants to play again.
    while play == 1:
        difficulty_level()
        play = play_again()
    # Prints out exiting message.
    print("Thank you for playing!")
    

# Prints out an initial statement explaining the game. This will not repeat if the player chooses to play again.
def starting_message():
    print("Welcome to the game of Hangman. I will pick a random word that you will then have to guess.")
    print("You will guess one letter at a time. If you make too many incorrect guesses, you lose.")
    print("But if you guess it right, you win!")

# Requests a difficulty level from the user, verifies the input, and plays the corresponding difficulty level.
def difficulty_level():
    # Initializes variable that will assign a number to useable answer.
    difficulty_option = 0
    # Allows for various versions of easy, medium, or hard.
    easy = ['easy', 'Easy', 'EASY', 'eASY', 'eaSY', 'easY', 'Easy', 'ESay', 'ESAy', 'esay']
    medium = ['medium', 'Medium', 'MEdium', 'MEDium', 'MEDIum', 'MEDIUm', 'MEDIUM', 'mediuM', 'mediUM', 'medIUM', 'meDIUM', 'mEDIUM', 'med', 'Med', 'MED']
    hard = ['hard', 'Hard', 'HArd', 'HARd', 'HARD', 'harD', 'haRD', 'hARD']
    # Requests a difficulty level from the user.
    difficulty = input("What difficulty level would you like to choose? You can choose 'easy', 'medium', or 'hard': ")
    # Checks if difficulty is chosen.
    for elem in easy:
        if difficulty == elem:
            difficulty_option = 1
    for elem in medium:
        if difficulty == elem:
            difficulty_option = 2
    for elem in hard:
        if difficulty == elem:
            difficulty_option = 3
    # If a difficulty is not chosen, the user is prompted until one is chosen.
    while difficulty_option != 1 and difficulty_option != 2 and difficulty_option != 3:
        # Asks user again for an answer.
        difficulty = input("Please choose 'easy', 'medium', or 'hard': ")
        # Checks if difficulty is chosen.
        for elem in easy:
            if difficulty == elem:
                difficulty_option = 1
        for elem in medium:
            if difficulty == elem:
                difficulty_option = 2
        for elem in hard:
            if difficulty == elem:
                difficulty_option = 3

    # Plays the corresponding difficulty level based on the answer given.
    if difficulty_option == 1:
        play_easy(difficulty)
    elif difficulty_option == 2:
        play_medium(difficulty)
    elif difficulty_option == 3:
        play_hard(difficulty)

# Produces the word that the user sees, which starts as a series of blanks.            
def show_word(chosen_word, stats):
    # Puts the word that the user sees into a list.
    word_shown = []
    # Adds a space for spaces in the word. Otherwise, the user will see a placeholder.
    for char in chosen_word:
        if char == " ":
            word_shown.append(' ')
        else:
            word_shown.append('_')
    # Returns the list that holds the same number of placeholders as the word to guess has letters.
    return word_shown

# Sets up the game to play on an easy level.
def play_easy(difficulty):
    # Adds 1 to base level of hints and guesses given.
    hints = MAX_HINTS + 1
    guesses = MAX_GUESSES + 1
    # Sets up the list that holds letters already guessed.
    letts_guessed = []
    # Sets up the dictionary that holds how many guesses and hints the player has used.
    stats = {'guesses_left': guesses, 'hints': hints}
    # Prints out a message explaining how the game is played with the easy setting.
    print("You chose easy. You get " + str(hints) + " hints and " + str(guesses) + " incorrect guesses.")
    print("The letters 'R' 'S' 'T' 'L' 'N' and 'E' have automatically been filled in for you.")
    print("If you want to use a hint, type 'hint' instead of a letter.")
    # Plays the game on easy.
    chosen_word = generate_word(difficulty)
    word_shown = show_word(chosen_word, stats)
    word_shown = pre_add_letters(chosen_word, word_shown, letts_guessed, stats)
    play_game(chosen_word, word_shown, hints, guesses, letts_guessed, stats)

# Sets up the game to play on a medium level.
def play_medium(difficulty):
    # Uses bases number of hints and guesses.
    hints = MAX_HINTS
    guesses = MAX_GUESSES
    # Sets up the list that holds letters already guessed.
    letts_guessed = []
    # Sets up the dictionary that holds how many guesses and hints the player has used.
    stats = {'guesses_left': guesses, 'hints': hints}
    # Prints out a message explaining how the game is played with the medium setting.
    print("You chose medium. You get " + str(hints) + " hint and " + str(guesses) + " incorrect guesses.")
    print("If you want to use a hint, type 'hint' instead of a letter.")
    # Plays the game on medium.
    chosen_word = generate_word(difficulty)
    word_shown = show_word(chosen_word, stats)
    play_game(chosen_word, word_shown, hints, guesses, letts_guessed, stats)

# Sets up the game to play on a hard level.
def play_hard(difficulty):
    # Subtracts 1 to base level of hints and guesses given.
    hints = MAX_HINTS - 1
    guesses = MAX_GUESSES - 1
    # Sets up the list that holds letters already guessed.
    letts_guessed = []
    # Sets up the dictionary that holds how many guesses and hints the player has used.
    stats = {'guesses_left': guesses, 'hints': hints}
    # Prints out a message explaining how the game is played with the hard setting.
    print("You chose hard. You get " + str(hints) + " hints and " + str(guesses) + " incorrect guesses. Good luck!")
    # Plays the game on hard.
    chosen_word = generate_word(difficulty)
    word_shown = show_word(chosen_word, stats)
    play_game(chosen_word, word_shown, hints, guesses, letts_guessed, stats)

# Fills in specific letters for the user before the user starts guessing. This is used for the easy difficulty level.
def pre_add_letters(chosen_word, word_shown, letts_guessed, stats):
    # Variable that tells the program how many times the letter has appeared in the word thus far.
    letter_appearance = 0
    # The letters that are being filled in for the user.
    given_letters = ['r', 's', 't', 'l', 'n', 'e']
    # Adds the letters that are being filled in to the letters already guessed to the user cannot try to guess one of these letters again.
    letts_guessed.extend(given_letters)
    # Loops through the word, looking at every character, to find one of the given letters.
    for char in chosen_word:
        if char == 'R' or char == 'S' or char == 'T' or char == 'L' or char == 'N' or char == 'E':
            # Replaces the blanks in the word shown with the letter being given within the word.
            if letter_appearance == 0:
                index = chosen_word.index(char)
                word_shown.pop(index)
                word_shown.insert(index, char)
                char = char.lower()
                letter_appearance += 1
            # If a letter appears more than one time, it will be inserted at its next appearance in the word.
            else:
                index = chosen_word.index(char, index + 1)
                word_shown.pop(index)
                word_shown.insert(index, char)
                letter_appearance += 1
    # Returns the word the user sees with the letters filled in.
    return word_shown

# Picks a random word from the word list for the user to guess based on difficulty level chosen.
def generate_word(difficulty):
    # Picks random word from list based on difficulty level.
    if difficulty == 'easy':
        number_in_list = random.randint(RANDOM_MIN_EASY, RANDOM_MAX_EASY)
    elif difficulty == 'medium':
        number_in_list = random.randint(RANDOM_MIN_MEDIUM, RANDOM_MAX_MEDIUM)
    else:
        number_in_list = random.randint(RANDOM_MIN_HARD, RANDOM_MAX_HARD)
    # Opens the word list and picks the word from the random number chosen.
    word_list = open('wordlist.txt')
    for i, line in enumerate(word_list):
        # Removes everything but the letters.
        if i == number_in_list:
            line = line.strip()
            chosen_word = line
    # Returns the word chosen.
    return chosen_word

# Runs the game by having the user guess a letter until they run out of guesses or guess the whole word.
def play_game(chosen_word, word_shown, hints, guesses, letts_guessed, stats):
    # Shows the word without any guesses yet given so the user can see how many letters are in it.
    # Will also show any pre-given characters.
    print("The word so far: " + ''.join(word_shown))
    # While the user still has guesses left and has not gotten the whole word, they will continue to guess a letter.
    while stats['guesses_left'] != 0 and collections.Counter(word_shown) != collections.Counter(chosen_word):
            letter_guessed = get_letter(letts_guessed, stats, chosen_word, word_shown)
            play_letter(letter_guessed, chosen_word, word_shown, stats)
    # Returns the word to be guessed and the dictionary containing how many guesses were left to show the results of the game.
    results(stats, chosen_word)

# Requests a letter from the user to guess.
def get_letter(letts_guessed, stats, chosen_word, word_shown):
    # Variable that tells the program how many times the letter has appeared in the word thus far.
    letter_appearance = 0
    # Requests a letter from the user
    letter_guessed = input("Enter the letter you would like to guess: ")
    # Checks if the user requested a hint.
    if letter_guessed == 'hint':
        letter_guessed = give_hint(stats, chosen_word, word_shown, letts_guessed)
    # Checks that only one letter was guessed.
    else:
        for char in letter_guessed:
            letter_appearance += 1
        # Checks that the letter has not already been guessed before.
        letter_guessed = no_repeats(letter_guessed, letts_guessed, stats, chosen_word, word_shown)
        # If more than one letter was guessed, the user is prompted to guess only one letter.
        while letter_appearance != 1:
            letter_guessed = input("Please enter only one letter: ")
            # Checks if the user requested a hint.
            if letter_guessed == 'hint':
                letter_guessed = give_hint(stats, chosen_word, word_shown, letts_guessed)
                letter_appearance = 1
            # If hint not requested, variable is continuously updated until only one letter is given.
            else:
                letter_appearance = 0
                for char in letter_guessed:
                    letter_appearance += 1
                # Checks that the letter has not already been guessed before.
                letter_guessed = no_repeats(letter_guessed, letts_guessed, stats, chosen_word, word_shown)
    # Returns the letter that the user guessed.
    return letter_guessed

# Checks if the user has any available hints, then gives the next letter in the word that has not yet been filled in.
def give_hint(stats, chosen_word, word_shown, letts_guessed):
    # Returns if no hints are available to the user.
    if stats['hints'] == 0:
            print("You have no more hints left.")
            blank = '_'
            return blank
    # Fills in the next blank letter for the user.
    else:
        # Searches for the next blank letter in the word.
        for char in word_shown:
            if char == '_':
                index = word_shown.index(char)
        # Replaces the blank in the word shown to the user with the appropriate letter.
        letter = chosen_word[index]
        word_shown.pop(index)
        word_shown.insert(index, letter)
        # Subtracts one hint.
        stats['hints'] -= 1
        # Adds the lowercase version of the letter to the letters already guessed.
        letter = letter.lower()
        letts_guessed.append(letter)
        # Tells the user how many hints they have left.
        print("You now have " + str(stats['hints']) + " hint(s) left.")
        # Returns the letter given as the hint.
        return letter

# Checks that the letter has not already been guessed or given as a hint or free letter.
def no_repeats(letter_guessed, letts_guessed, stats, chosen_word, word_shown):
    # Requests a new letter from the user if they chose a letter already guessed.
    while letter_guessed.lower() in letts_guessed:
        letter_guessed = input("You have already guessed this letter. Please pick a different letter: ")
    # Checks if the user requested a hint.
    if letter_guessed == 'hint':
        letter_guessed = give_hint(stats, chosen_word, word_shown, letts_guessed)
    # Adds the lowercase version of the letter to the letters already guessed.
    letter_guessed = letter_guessed.lower()
    letts_guessed.append(letter_guessed)
    # Returns the letter guessed.
    return letter_guessed

# Plays the letter given by the user. 
# If the letter is wrong, the stats are updated. 
# If the letter is right, it is inserted into the word shown to the user.
def play_letter(letter_guessed, chosen_word, word_shown, stats):
    # Variable that tells the program how many times the letter has appeared in the word thus far.
    letter_appearance = 0
    # Loops through the word, looking at every character, to see if the letter given by the user is in the word.
    for char in chosen_word:
        # Compares the lowercase value of the letter given and the letter in the word.
        if letter_guessed.lower() == char.lower():
            # Replaces the blanks in the word shown with the letter that was guessed.
            if letter_appearance == 0:
                index = chosen_word.index(char)
                word_shown.pop(index)
                word_shown.insert(index, char)
                letter_appearance += 1
            # If a letter appears more than one time, it will be inserted at its next appearance in the word.
            else:
                index = chosen_word.index(char, index + 1)
                word_shown.pop(index)
                word_shown.insert(index, char)
                letter_appearance += 1
    # If a hint was requested but no hints were available, this ensures it is not marked as an incorrect answer.
    if letter_guessed == '_':
        letter_appearance += 1
    # If the letter guessed is not in the word, the user is told with the new number of incorrect guesses left.
    if letter_appearance == 0:

        # Subtracts oen from the number of incorrect guesses the user has left.
        stats['guesses_left'] -= 1
        # Tells the user that the letter is not in the word and gives them how many incorrect guesses they have left.
        print("Incorrect. You now have " + str(stats['guesses_left']) + " incorrect guesses left.")
    # Prints the word so far.
    print("The word so far: " + ''.join(word_shown))

# Prints out whether the user won or lost the game.
def results(stats, chosen_word):
    # Prints a message if the user ran out of guesses and shows the full word.
    if stats['guesses_left'] == 0:
        print("You ran out of guesses. The word was " + chosen_word + ". Better luck next time!")
    # Prints a message that the user correctly guessed the word.
    else:
        print("Congratulations! You won!")

# Asks the user if they want to replay the game.
def play_again():
    # Initializes variable that will assign a number to useable answer.
    play = 0
    # Allows user to answer various verions of 'yes' and 'no'
    yes = ['y', 'Y', 'yes', 'Yes', 'YEs', 'YES', 'yES', 'yse']
    no = ['n', 'N', 'no', 'No', 'nO', 'NO']
    # Asks the user if they want to replay the game.
    replay = input("Do you want to play again?: ")
    # Checks if yes or no is given.
    for elem in yes:
        if replay == elem:
            play = 1
    for elem in no:
        if replay == elem:
            play = 2
    # If a yes or no is not given, the user is asked again until an option is chosen.
    while play != 1 and play != 2:
        # Asks the user again for an answer.
        replay = input("Please choose 'yes' or 'no': ")
        # Checks if yes or no is given
        for element in yes:
            if replay == element:
                play = 1
        for element in no:
            if replay == element:
                play = 2
    # Returns answer given by user.        
    return play    

if __name__ == '__main__':
    main()
