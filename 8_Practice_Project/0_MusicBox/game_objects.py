from random import randint


class Question:

    def __init__(self, note_1: str, note_2: str, semitone_count: int):
        self.note_1 = note_1
        self.note_2 = note_2
        self.semitone_count = semitone_count

    def check_answer(self, answer):
        return answer == self.semitone_count


class RandomNumbers:

    def __init__(self, rand_number_1: int, rand_number_2: int, randon_numbers: tuple) -> tuple:
        self.rand_number_1 = rand_number_1
        self.rand_number_2 = rand_number_2
        self.random_numbers = randon_numbers

