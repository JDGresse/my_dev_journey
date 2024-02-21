"""
A game that tests and grows music theory knowledge by randomly generating two different notes, and players have to guess how many semi-tones are between these two notes.

main.py controls the game and imports predefinded string-messages, objects and functions from message.py and game_mechanics.py respectively.

For a more detailed explanation see MyREADME.md
"""

from messages import welcome, game_rules

from game_functions import get_next_question
from game_objects import RandomNumbers, Question
from game_variables import notes


# refactor-ross variables
player_answer: str = None

# Declare variables
counter: int = 0
game: bool = True
game_notes: list[any] = [None, None, None]
correct = False

## Start game ##

# Ask players if they want to view the rules
rules: str = input(welcome)
if rules.lower() == "rules":
    input(game_rules)

print("\nLet's play!\n")

# Game Looop
while game == True:

    # Check if it is the first game
    if counter == 0:
        counter += 1

        # Generate game notes
        question = Question

        # Call generate_random_number here rather than in main.py
        random_numbers = get_next_question()

        question.note_1 = notes[random_numbers[0]][0]
        question.note_2 = notes[random_numbers[1]][0]
        question.semitone_count = abs(notes[random_numbers[0]][1] - notes[random_numbers[1]][1])

        # Check player answer
        while question.check_answer(player_answer) == False:

            # Capture player answer
            player_answer: str = input(f"The two notes are:\n{question.note_1} and\n{question.note_2}\n\nHow many semitones seperate them:\n")

            # check if the player wants to quit | give up:
            if player_answer == 'done':
                print(f"\nThe answer you where looking for is: {question.semitone_count}\n")
                break
            else:
                # Incorrect answer
                print("\nSorry!\nYour answer is NOT correct.\n")

        # Correct answer
        print("\nGOOD JOB!\nYour answer is correct.\n")

    else:
        # Ask if the player would like to play agin
        play_more: str = input("Would you like to play again? (y/n):\n")
        # Exit game
        if play_more.lower() == 'n' or play_more.lower() == 'no':
            print("Thank you for playing Music Box!\nWe hope to see you soon.\n\n")
            game = False
        # Reset loop and play again
        else:
            counter = 0
            correct = False