import unittest
from model.board import Board


class TestBoard(unittest.TestCase):
    # Prueba Statement Coverage: Validar inicialización correcta
    def test_board_initialization(self):
        board = Board(1)
        self.assertEqual(board.size, 6)
        self.assertEqual(board.total_bombs, 8)

        board = Board(2)
        self.assertEqual(board.size, 8)
        self.assertEqual(board.total_bombs, 16)

        board = Board(3)
        self.assertEqual(board.size, 10)
        self.assertEqual(board.total_bombs, 32)
    
    # Prueba valores límite: Dificultades fuera de rango
    def test_invalid_difficulty(self):
        with self.assertRaises(ValueError): # Frontera inferior
            Board(0)

        with self.assertRaises(ValueError): # Frontera superior
            Board(4)

    # Loop Testing: Verificar conteo de bombas
    def test_bomb_counting(self):
        board = Board(1)
        total_bombs = sum(tile.is_bomb for row in board.tiles for tile in row)
        self.assertEqual(total_bombs, board.total_bombs)

    # Path Coverage: Verificar revelado de casilla
    def test_reveal_tile(self):
        board = Board(1)
        board.reveal_tile(0, 0)
        self.assertTrue(board.tiles[0][0].is_revealed)

    # Decision Coverage: Perder tras descubrir una bomba
    def test_game_lost_condition(self):
        board = Board(1)
        for x in range(board.size):
            for y in range(board.size):
                if board.tiles[x][y].is_bomb:
                    board.reveal_tile(x, y)  
                    break
        self.assertTrue(board.is_game_lost)

    # Loop Testing y Path Coverage: Ganar tras revelar todas las no-bombas
    def test_game_win_condition(self):
        board = Board(1)
        for row in board.tiles:
            for tile in row:
                if not tile.is_bomb:
                    tile.reveal()
        self.assertTrue(board.is_game_won())


if __name__ == "__main__":
    unittest.main()


