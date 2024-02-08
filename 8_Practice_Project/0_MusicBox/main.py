"""
A game that tests and grows music theory knowledge by randomly generating two different notes, and players have to guess how many semi-tones are between these two notes.

main.py controls the game and imports predefinded string-messages, objects and functions from message.py and game_mechanics.py respectively.

For a more detailed explanation see MyREADME.md
"""

from messages import welcome, game_rules
from game_mechanics import random_note_generator, check_player_answer

# Declare variables
counter: int = 0
game: bool = True
game_notes: list[any] = [None, None]
correct = False

## Start game ##

# Ask players if they want to view the rules
rules: str = input(welcome)
if rules.lower() == "rules":
    input(game_rules)

print("Let's play!")

# Game Looop
while game == True:

    # Check if it is the first game
    if counter == 0:
        counter += 1
        # Generate game notes
        game_notes = random_note_generator()

        # Check player answer
        while correct == False:

            # Capture player answer
            player_answer: str = input(f"The two notes are:\n{game_notes[0]} and\n{game_notes[1]}\n\nHow many semitones seperate them:\n")

            # Check if the player is done playing
            if player_answer.lower() == "done":
                print("Thank you for playing Music Box!\nWe hope to see you soon.\n\n")
                correct = True
                game = False
            else:
                # check the players answer and dislay the corresponding message and True - for correct - or False - for incorrect - answers
                correct = check_player_answer(int(player_answer), game_notes[2])

    else:
        # Ask if the player would like to play agin
        play_more: str = input("Would you like to play again? (y/n):\n")
        if play_more.lower() == 'n' or play_more.lower() == 'no':
            print("Thank you for playing Music Box!\nWe hope to see you soon.\n\n")
            game = False
        else:
            counter = 0
            correct = False