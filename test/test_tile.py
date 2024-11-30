import unittest
from model.tile import Tile


class TestTile(unittest.TestCase):
    # Prueba de Particiones Equivalentes: Estado inicial
    def test_tile_initialization(self):
        tile = Tile()
        self.assertFalse(tile.is_bomb)  # No debe ser bomba
        self.assertFalse(tile.is_revealed)  # No debe estar revelada
        self.assertEqual(tile.neighboring_bombs, 0)  # Vecinas deben ser 0

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
        self.assertEqual(tile.display(), " ")  # Sin revelar, muestra espacio

        tile.reveal()
        self.assertEqual(tile.display(), "0")  # Revelada sin bomba muestra 0

        # Crear un nuevo tile o reiniciar el estado
        tile = Tile()
        tile.is_bomb = True
        tile.reveal()
        self.assertEqual(tile.display(), "X")  # Revelada con bomba muestra X

    # Valores Límite: Vecinas = 0
    def test_neighboring_bombs_zero(self):
        tile = Tile()
        tile.neighboring_bombs = 0
        tile.reveal()
        self.assertEqual(tile.display(), "0")  # Sin bombas vecinas muestra 0

    # Valores Límite: Vecinas = 1
    def test_neighboring_bombs_one(self):
        tile = Tile()
        tile.neighboring_bombs = 1
        tile.reveal()
        self.assertEqual(tile.display(), "1")  # Una bomba vecina muestra 1

    # Valores Límite: Vecinas = 8
    def test_neighboring_bombs_eight(self):
        tile = Tile()
        tile.neighboring_bombs = 8
        tile.reveal()
        self.assertEqual(tile.display(), "8")  # Ocho bombas vecinas muestra 8

    # Pairwise Testing: Combinaciones de estados
    def test_pairwise_combinations(self):
        tile = Tile()

        # No bomba, no revelada
        tile.is_bomb = False
        tile.is_revealed = False
        tile.neighboring_bombs = 0
        self.assertEqual(tile.display(), " ")

        # No bomba, revelada
        tile.is_bomb = False
        tile.is_revealed = True
        tile.neighboring_bombs = 3
        self.assertEqual(tile.display(), "3")

        # Bomba, no revelada
        tile.is_bomb = True
        tile.is_revealed = False
        self.assertEqual(tile.display(), " ")

        # Bomba, revelada
        tile.is_bomb = True
        tile.is_revealed = True
        self.assertEqual(tile.display(), "X")


if __name__ == "__main__":
    unittest.main()
