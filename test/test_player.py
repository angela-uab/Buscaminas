import pytest
from model.player import Player

import unittest

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(1, "Alice", 10)

    def test_initialization(self):
        self.assertEqual(self.player.get_id(), 1)
        self.assertEqual(self.player.get_name(), "Alice")
        self.assertEqual(self.player.get_score(), 10)

    def test_set_id_valid(self):
        self.player.set_id(2)
        self.assertEqual(self.player.get_id(), 2)

    def test_set_invalid_id_type(self):
        with self.assertRaises(ValueError):
            self.player.set_id("invalid_id")

    def test_set_invalid_id_negative(self):
        with self.assertRaises(ValueError):
            self.player.set_id(-1)

    def test_set_name_valid(self):
        self.player.set_name("Bob")
        self.assertEqual(self.player.get_name(), "Bob")

    def test_set_invalid_name_type(self):
        with self.assertRaises(ValueError):
            self.player.set_name(123)

    def test_set_invalid_name_empty(self):
        with self.assertRaises(ValueError):
            self.player.set_name("")

    def test_set_score_valid(self):
        self.player.set_score(50)
        self.assertEqual(self.player.get_score(), 50)

    def test_set_invalid_score_type(self):
        with self.assertRaises(ValueError):
            self.player.set_score("invalid_score")

    def test_set_invalid_score_negative(self):
        with self.assertRaises(ValueError):
            self.player.set_score(-10)

    def test_get_name_after_invalid_set(self):
        with self.assertRaises(ValueError):
            self.player.set_name("")
        self.assertEqual(self.player.get_name(), "Alice")  

if __name__ == '__main__':
    unittest.main()
