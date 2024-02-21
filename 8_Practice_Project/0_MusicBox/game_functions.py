"""
game_mechanics.py contains all of the functions and classes used to run each aspect of the game.
"""
from game_variables import notes
from game_objects import Question, RandomNumbers

# Variables
notes: tuple = (
    ("A", 0),
    ("A#", 1),
    ("Bb", 1),
    ("B", 2),
    ("C", 3),
    ("C#", 4),
    ("Db", 4),
    ("D", 5),
    ("D#", 6),
    ("Eb", 6),
    ("E", 7),
    ("F", 8),
    ("F#", 9),
    ("Gb", 9),
    ("G", 10),
    ("G#", 11),
    ("Ab", 11),
)


def get_next_question() -> Question: # Question is custom class I created
    """
    Function that extract game notes from the notes dictionary.

    Returns:
        list[str]: = [game-note-1, game-note-2, correct-answer]
        ex: ['Gb', 'E', 6]
    """
    question = Question

    # Call generate_random_number here rather than in main.py
    random_numbers: tuple[int, int] = RandomNumbers

    question.note_1 = notes[random_numbers[0]][0]
    question.note_2 = notes[random_numbers[1]][0]
    question.semitone_count = abs(notes[random_numbers[0]][1] - notes[random_numbers[1]][1])

    return question