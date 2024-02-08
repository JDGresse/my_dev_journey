"""
Tests to ensure that music theory game developed in main.py function as expected.
"""

import unittest

from game_mechanics import random_note_generator, check_player_answer


class TestMusicBox(unittest.TestCase):
    """Test the functionality of the Music Box game."""

    # Setup variables required for testing
    def setUp(self):
        self.correct_answer: int = 3
        self.incorrect_answer: int = 5


    def test_random_note_generator_unique(self):
        """
        Test that the random_note_generator returns two random notes.
        """
        notes_unique: list[str] = random_note_generator()
        self.assertIsNot(notes_unique[0], notes_unique[1])

    def test_check_palyer_answer_correct(self):
        """Test that the check_player_answer function correctly evaluates correct answers."""
        correct_answer: bool = check_player_answer(self.correct_answer, self.correct_answer)
        self.assertTrue(correct_answer)

    def test_check_palyer_answer_incorrect(self):
        """Test that the check_player_answer function correctly evaluates incorrect answers."""
        incorrect_answer: bool = check_player_answer(self.incorrect_answer, self.correct_answer)
        self.assertFalse(incorrect_answer)
