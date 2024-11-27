import unittest
from model.tile import Tile


class TestTile(unittest.TestCase):
    def test_tile_initialization(self):
        tile = Tile()
        self.assertFalse(tile.is_bomb)
        self.assertFalse(tile.is_revealed)
        self.assertEqual(tile.neighboring_bombs, 0)

    def test_tile_set_bomb(self):
        tile = Tile()
        tile.is_bomb = True
        self.assertTrue(tile.is_bomb)

    def test_tile_reveal(self):
        tile = Tile()
        tile.reveal()
        self.assertTrue(tile.is_revealed)

    def test_tile_display(self):
        tile = Tile()
        self.assertEqual(tile.display(), " ")

        tile.reveal()
        self.assertEqual(tile.display(), "0")

        tile.is_bomb = True
        tile.reveal()
        self.assertEqual(tile.display(), "X")


if __name__ == "__main__":
    unittest.main()
