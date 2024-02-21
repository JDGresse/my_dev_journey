"""
messages.py contains all of the messages displayed to players during the game.
"""

"""Welcome message."""
welcome: str = (
    "Welcome to Music Box, a game that helps you learn music theory.\n\nIf this is your first time playing, \nOr if you would like a recap of the rules, please enter 'rules'.\n\nOr, if you are ready to play, press any key to continue!\n"
)


"""Game rules."""
game_rules: str = "Game Rules:\n\nWhen the game starts, you will be presented with two random notes, eg. A# and Eb. You then need to count the number of semitones between these two notes (5 in this example) and enter your answer.\n\n Semitones are counted from A -> G#/Ab, with A = 0, and G#/Ab = 12.\nThe game will then let you know if your answer is correct or incorrect.\nIf your answer is incorrect, you can immediately enter another answer and continue the game, until you enter the correct answer, or decide you have played enough.\n\nYou can end your game AT ANY TIME by entering 'done' instead of an answer.\n\nIf you are busy playing a game, but have not entered a correct answer yet, entering 'done' will display the correct answer, and give you the option to play again.\n\nPress any key to continue."
