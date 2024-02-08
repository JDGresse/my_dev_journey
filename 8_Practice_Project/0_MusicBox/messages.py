"""
messages.py contains all of the messages displayed to players during the game.
"""

"""Welcome message."""
welcome: str = (
    "Welcome to Music Box, a game that helps you learn music theory.\n\nIf this is your first time playing, \nOr if you would like a recap of the rules, please enter 'rules'.\n\nOr, if you are ready to play, press any key to continue!\n"
)


"""Game rules."""
game_rules: str = "Game Rules:\n\nWhen the game starts, you will be presented with two random notes, ex A# and Eb. You then count the number of semitones between these two notes (5 in this example) and enter your answer. The game will then let you know if your answer is correct or incorrect.\n\nIf your answer is incorrect, you can immediately enter another answer and continue the game, until you enter the correct answer, or decide you have played enough.\n\nYou can end your game at any time by entering 'done' instead of an answer.\n\nPress any key to continue."
