import unittest
from model.tile import Tile


class TestTile(unittest.TestCase):
    # Prueba de Particiones Equivalentes: Estado inicial
    def test_tile_initialization(self):
        tile = Tile()
        self.assertFalse(tile.is_bomb)
        self.assertFalse(tile.is_revealed)
        self.assertEqual(tile.neighboring_bombs, 0)

    # Prueba Statement Coverage: Establecer bomba
    def test_tile_set_bomb(self):
        tile = Tile()
        tile.is_bomb = True
        self.assertTrue(tile.is_bomb)

    # Decision Coverage: Revelar casilla
    def test_tile_reveal(self):
        tile = Tile()
        tile.reveal()
        self.assertTrue(tile.is_revealed)

    # Pairwise Testing: Combinaciones posibles de `is_bomb` y `is_revealed`
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
