import unittest
from unittest.mock import patch
from model.board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(1)  # Inicializar el tablero con dificultad 1 para todos los tests

    # Prueba Statement Coverage: Validar inicialización correcta
    def test_board_initialization(self):
        self.assertEqual(self.board.size, 6)
        self.assertEqual(self.board.total_bombs, 8)

        board2 = Board(2)
        self.assertEqual(board2.size, 8)
        self.assertEqual(board2.total_bombs, 16)

        board3 = Board(3)
        self.assertEqual(board3.size, 10)
        self.assertEqual(board3.total_bombs, 32)

    # Prueba valores límite: Dificultades fuera de rango
    def test_invalid_difficulty(self):
        with self.assertRaises(ValueError):  # Frontera inferior
            Board(0)

        with self.assertRaises(ValueError):  # Frontera superior
            Board(4)

    # Loop Testing: Verificar conteo de bombas
    def test_bomb_counting(self):
        total_bombs = sum(tile.is_bomb for row in self.board.tiles for tile in row)
        self.assertEqual(total_bombs, self.board.total_bombs)

    # Path Coverage: Verificar revelado de casilla
    def test_reveal_tile(self):
        success = self.board.reveal_tile(0, 0)
        self.assertTrue(self.board.tiles[0][0].is_revealed)
        self.assertTrue(success)

    # Decision Coverage: Perder tras descubrir una bomba
    def test_game_lost_condition(self):
        for x in range(self.board.size):
            for y in range(self.board.size):
                if self.board.tiles[x][y].is_bomb:
                    self.board.reveal_tile(x, y)
                    self.assertTrue(self.board.is_game_lost)
                    return

    # Loop Testing y Path Coverage: Ganar tras revelar todas las no-bombas
    def test_game_win_condition(self):
        for row in self.board.tiles:
            for tile in row:
                if not tile.is_bomb:
                    tile.reveal()
        self.assertTrue(self.board.is_game_won())

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

    # Prueba funcional: Verifica la validación de coordenadas
    def test_get_valid_coordinates(self):
        def mock_input(prompt):
            return "1 1"  # Mock para simular coordenadas válidas

        with patch("builtins.input", mock_input):
            x, y = self.board.get_valid_coordinates()
            self.assertEqual((x, y), (0, 0))  # Ajustado por índice basado en 0

    # Path Coverage: Revelar una casilla ya revelada
    def test_reveal_already_revealed_tile(self):
        self.board.tiles[0][0].reveal()  # Revelar la casilla primero
        result = self.board.reveal_tile(0, 0)
        self.assertFalse(result)  # Intentar revelar de nuevo debe devolver False

    # Loop Testing: Verifica que el número de bombas esté dentro de los límites
    def test_bomb_count_within_bounds(self):
        bomb_count = sum(tile.is_bomb for row in self.board.tiles for tile in row)
        self.assertLessEqual(bomb_count, self.board.size * self.board.size)  # Bombas no deben exceder casillas totales

    # Decision Coverage: Tablero sin bombas debería ganar automáticamente
    def test_empty_board(self):
        for row in self.board.tiles:
            for tile in row:
                tile.is_bomb = False
                tile.reveal()  # Revelar todas las casillas
        self.assertTrue(self.board.is_game_won())  # Todas las casillas son seguras, debería ganar
    
    # Condition Coverage: Validar coordenadas (valores válidos e inválidos)
    def test_validate_coordinates(self):
        # Ambas condiciones verdaderas
        x, y = 0, 0
        self.assertTrue(0 <= x < self.board.size and 0 <= y < self.board.size)

        # Primera condición falsa
        x, y = -1, 0
        self.assertFalse(0 <= x < self.board.size and 0 <= y < self.board.size)

        # Segunda condición falsa
        x, y = 0, self.board.size
        self.assertFalse(0 <= x < self.board.size and 0 <= y < self.board.size)

        # Ambas condiciones falsas
        x, y = -1, self.board.size
        self.assertFalse(0 <= x < self.board.size and 0 <= y < self.board.size)


if __name__ == "__main__":
    unittest.main()
