"""
game_mechanics.py contains all of the functions and classes used to run each aspect of the game.
"""
from random import randint

# Variables
notes: dict = {
    0: "A",
    1: "A#",
    2: "Bb",
    3: "B",
    4: "C",
    5: "C#",
    6: "Db",
    7: "D",
    8: "D#",
    9: "Eb",
    10: "E",
    11: "F",
    12: "F#",
    13: "Gb",
    14: "G",
    15: "G#",
    16: "Ab",
}


def random_note_generator() -> list[str]:
    """
    Function that generate two random and unique notes.

    Returns:
        list[str]: = [str=note-1, str=note-2]
        ex: ["A", "C"]
    """
    return_list: list = ["", "", 0]
    note_position: list = [0, 0]
    random_numbers: list = [None, None]

    # Generate unique random numbers
    random_numbers[0] = randint(0, 16)
    random_numbers[1] = randint(0, 16)
    while random_numbers[0] == random_numbers[1]:
        random_numbers[1] = randint(0, 16)

    # Convert to notes
    for i in range(2):
        match random_numbers[i]:
            case 0:
                return_list[i] = notes[0]
                note_position[i] = 0
            case 1:
                return_list[i] = notes[1]
                note_position[i] = 1
            case 2:
                return_list[i] = notes[2]
                note_position[i] = 1
            case 3:
                return_list[i] = notes[3]
                note_position[i] = 2
            case 4:
                return_list[i] = notes[4]
                note_position[i] = 3
            case 5:
                return_list[i] = notes[5]
                note_position[i] = 4
            case 6:
                return_list[i] = notes[6]
                note_position[i] = 4
            case 7:
                return_list[i] = notes[7]
                note_position[i] = 5
            case 8:
                return_list[i] = notes[8]
                note_position[i] = 6
            case 9:
                return_list[i] = notes[9]
                note_position[i] = 6
            case 10:
                return_list[i] = notes[10]
                note_position[i] = 7
            case 11:
                return_list[i] = notes[11]
                note_position[i] = 8
            case 12:
                return_list[i] = notes[12]
                note_position[i] = 9
            case 13:
                return_list[i] = notes[13]
                note_position[i] = 9
            case 14:
                return_list[i] = notes[14]
                note_position[i] = 10
            case 15:
                return_list[i] = notes[15]
                note_position[i] = 11
            case 16:
                return_list[i] = notes[16]
                note_position[i] = 11
            case _ :
                "No matches found"

    # Calculate answer
    return_list[2] = abs(note_position[0] - note_position[1])

    return return_list

def check_player_answer(player_answer: int, correct_answer: int) -> bool:
    """
    Check if the player answer is correct.

    Args:
        player_answer (int): player guess/answer for the number of semitones between the game notes
        correct_answer (int): correct number of semitones between game notes

    Returns:
        bool:   corret answer -> True
                incorrect answer -> False
    """
    if player_answer == correct_answer:
        print("GOOD JOB!\nYour answer is correct.\n")
        return True
    else:
        print("Sorry!\nYour answer is NOT correct.\n")
        return False