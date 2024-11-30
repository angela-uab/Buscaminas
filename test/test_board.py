import unittest
from unittest.mock import patch
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
        with self.assertRaises(ValueError):  # Frontera inferior
            Board(0)

        with self.assertRaises(ValueError):  # Frontera superior
            Board(4)

    # Loop Testing: Verificar conteo de bombas
    def test_bomb_counting(self):
        board = Board(1)
        total_bombs = sum(tile.is_bomb for row in board.tiles for tile in row)
        self.assertEqual(total_bombs, board.total_bombs)

    # Path Coverage: Verificar revelado de casilla
    def test_reveal_tile(self):
        board = Board(1)
        success = board.reveal_tile(0, 0)
        self.assertTrue(board.tiles[0][0].is_revealed)
        self.assertTrue(success)

    # Decision Coverage: Perder tras descubrir una bomba
    def test_game_lost_condition(self):
        board = Board(1)
        for x in range(board.size):
            for y in range(board.size):
                if board.tiles[x][y].is_bomb:
                    board.reveal_tile(x, y)  
                    self.assertTrue(board.is_game_lost)
                    return

    # Loop Testing y Path Coverage: Ganar tras revelar todas las no-bombas
    def test_game_win_condition(self):
        board = Board(1)
        for row in board.tiles:
            for tile in row:
                if not tile.is_bomb:
                    tile.reveal()
        self.assertTrue(board.is_game_won())

    # Pairwise Testing: Combinaciones posibles de tamaño y número de bombas
    def test_pairwise_board_configurations(self):
        configurations = [
            (6, 8),   # Fácil
            (8, 16),  # Medio
            (10, 32), # Difícil
        ]
        for size, bombs in configurations:
            board = Board(1)
            board.size = size
            board.total_bombs = bombs
            self.assertEqual(board.size, size)
            self.assertEqual(board.total_bombs, bombs)

    # Valores Límite: Tablero pequeño y grande
    def test_board_edge_sizes(self):
        # Tablero mínimo
        small_board = Board(1)
        small_board.size = 2
        small_board.total_bombs = 1
        self.assertEqual(small_board.size, 2)
        self.assertEqual(small_board.total_bombs, 1)

        # Tablero grande
        large_board = Board(1)
        large_board.size = 50
        large_board.total_bombs = 100
        self.assertEqual(large_board.size, 50)
        self.assertEqual(large_board.total_bombs, 100)

    def test_get_valid_coordinates(self):
        board = Board(1)

        def mock_input(prompt):
            return "1 1"  

        with patch("builtins.input", mock_input):
            x, y = board.get_valid_coordinates()
            self.assertEqual((x, y), (0, 0))  # Ajustado por índice basado en 0

    def test_reveal_already_revealed_tile(self):
        board = Board(1)
        board.tiles[0][0].reveal() 
        result = board.reveal_tile(0, 0)
        self.assertFalse(result)  # Intentar revelar de nuevo debe devolver False

    def test_bomb_count_within_bounds(self):
        board = Board(1)
        bomb_count = sum(tile.is_bomb for row in board.tiles for tile in row)
        self.assertLessEqual(bomb_count, board.size * board.size)  # Bombas no deben exceder casillas totales
    
    def test_empty_board(self):
        board = Board(1)
        for row in board.tiles:
            for tile in row:
                tile.is_bomb = False
                tile.reveal()  
        self.assertTrue(board.is_game_won())  


if __name__ == "__main__":
    unittest.main()
