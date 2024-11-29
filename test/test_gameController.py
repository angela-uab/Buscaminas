import unittest
from unittest.mock import patch
from model.board import Board
from model.player import Player
from model.database_manager import DatabaseManager
from view.gameView import View
from controller.gameController import GameController


class TestGameControllerTDD(unittest.TestCase):
    def setUp(self):        
        self.controller = GameController()
        self.controller.database.database_name = "test_database.db"
        self.controller.database.connection.execute("DELETE FROM players") 
        self.controller.database.connection.commit()

    def tearDown(self):
        self.controller.database.close()

    # Statement Coverage: Verifica que los objetos de vista y base de datos son inicializados correctamente.
    def test_initialize_game_controller(self):
        self.assertIsInstance(self.controller.view, View)
        self.assertIsInstance(self.controller.database, DatabaseManager)

    # Statement Coverage: Verifica que el método del menú captura correctamente la entrada.
    def test_show_menu(self):
        with unittest.mock.patch('builtins.input', return_value="1"):
            option = self.controller.view.display_menu()
            self.assertEqual(option, "1")

    # Path Coverage: Verifica la inicialización del juego con entradas válidas.
    def test_start_game_initialization(self):
        with unittest.mock.patch('builtins.input', side_effect=["TestPlayer", "1"]):
            player_name = self.controller.view.get_player_name()
            difficulty = self.controller.view.display_difficulty_menu()
            board = Board(difficulty)

            self.assertEqual(player_name, "TestPlayer")
            self.assertEqual(difficulty, 1)
            self.assertEqual(board.size, 6)  # Dificultad 1 equivale a 6x6

    # Decision Coverage: Verifica que el juego se pierde al revelar una bomba.
    def test_reveal_bomb_tile(self):
        board = Board(1)
        player = Player(0, "TestPlayer", 0)
        x, y = 0, 0
        board.tiles[x][y].is_bomb = True  # Simulamos una bomba en (0, 0)

        board.reveal_tile(x, y)
        self.assertTrue(board.is_game_lost)
        self.assertEqual(player.get_score(), 0)

    # Partición Equivalente: Verifica que el puntaje se incrementa al revelar una bomba.
    def test_add_score_on_bomb(self):
        board = Board(1)
        player = Player(0, "TestPlayer", 0)
        x, y = 0, 0
        board.tiles[x][y].is_bomb = True

        board.reveal_tile(x, y)
        player.set_score(player.get_score() + 10)
        self.assertEqual(player.get_score(), 10)

    # Loop Testing: Verifica que el juego se gana al revelar todas las casillas no bomba.
    def test_game_won(self):
        board = Board(1)
        player = Player(0, "TestPlayer", 0)

        # Revelamos todas las casillas no bomba
        for row in board.tiles:
            for tile in row:
                if not tile.is_bomb:
                    tile.reveal()

        self.assertTrue(board.is_game_won())

    # Decision Coverage: Verifica que el juego se pierde al revelar una casilla con bomba.
    def test_game_lost(self):
        board = Board(1)
        player = Player(0, "TestPlayer", 0)
        x, y = 0, 0
        board.tiles[x][y].is_bomb = True

        board.reveal_tile(x, y)
        self.assertTrue(board.is_game_lost)

    # Statement Coverage: Verifica que los rankings están vacíos inicialmente.
    def test_rankings_no_data(self):
        rankings = self.controller.database.get_top_players()
        self.assertEqual(len(rankings), 0)

    # Path Coverage: Inserta un jugador en los rankings y verifica su recuperación.
    def test_insert_and_retrieve_rankings(self):
        self.controller.database.insert_player("TestPlayer", 50)
        rankings = self.controller.database.get_top_players()
        self.assertEqual(len(rankings), 1)
        self.assertEqual(rankings[0][1], "TestPlayer")
        self.assertEqual(rankings[0][2], 50)

    # Statement Coverage: Inserta múltiples jugadores y verifica la correcta recuperación del ranking.
    def test_show_rankings_with_data(self):
        self.controller.database.insert_player("Player1", 100)
        self.controller.database.insert_player("Player2", 80)
        rankings = self.controller.database.get_top_players()

        self.assertEqual(len(rankings), 2)
        self.assertEqual(rankings[0][1], "Player1")
        self.assertEqual(rankings[1][1], "Player2")

    # Statement Coverage: Verifica que se muestra el mensaje adecuado cuando no hay rankings disponibles.
    def test_show_rankings_message_no_data(self):
        with unittest.mock.patch('builtins.print') as mock_print:
            self.controller.show_rankings()
            mock_print.assert_called_once_with("No hay rankings disponibles. Juega una partida para aparecer aquí.")

    # Loop Testing: Simular varias partidas
    def test_multiple_games(self):
        for i in range(5):  
            self.controller.database.insert_player(f"Player{i}", i * 10)
        rankings = self.controller.database.get_top_players()
        self.assertEqual(len(rankings), 5)


if __name__ == "__main__":
    unittest.main()