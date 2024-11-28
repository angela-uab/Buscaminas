import unittest
from unittest.mock import patch, MagicMock
from controller.gameController import GameController
from model.board import Board
from model.player import Player
from model.database_manager import DatabaseManager


class TestGameController(unittest.TestCase):
    @patch("controller.gameController.View")
    @patch("controller.gameController.Board")
    @patch("controller.gameController.DatabaseManager")
    def test_start_game(self, mock_database_manager, mock_board, mock_view):
        
        mock_view.return_value.display_menu.return_value = "1"
        mock_view.return_value.get_player_name.return_value = "TestPlayer"
        mock_view.return_value.display_difficulty_menu.return_value = 1
        mock_view.return_value.get_coordinates.return_value = (1, 1)
        mock_board.return_value.size = 6
        mock_board.return_value.tiles = [[MagicMock(is_bomb=False) for _ in range(6)] for _ in range(6)]
        mock_board.return_value.is_game_won.return_value = True
        mock_database_manager.return_value.insert_player.return_value = True

        
        controller = GameController()
        controller.run()

        
        mock_view.return_value.get_player_name.assert_called_once()
        mock_view.return_value.display_difficulty_menu.assert_called_once()
        mock_view.return_value.display_board.assert_called()
        mock_database_manager.return_value.insert_player.assert_called_once_with("TestPlayer", 0)

    @patch("controller.gameController.View")
    @patch("controller.gameController.DatabaseManager")
    def test_show_rankings_with_data(self, mock_database_manager, mock_view):
        
        mock_database_manager.return_value.get_top_players.return_value = [
            (1, "Player1", 100),
            (2, "Player2", 80),
        ]
        mock_view.return_value.display_menu.return_value = "2"

        
        controller = GameController()
        controller.run()

        
        mock_view.return_value.display_rankings.assert_called_once_with(
            [(1, "Player1", 100), (2, "Player2", 80)]
        )

    @patch("controller.gameController.View")
    @patch("controller.gameController.DatabaseManager")
    def test_show_rankings_no_data(self, mock_database_manager, mock_view):
        
        mock_database_manager.return_value.get_top_players.return_value = []
        mock_view.return_value.display_menu.return_value = "2"

        
        controller = GameController()
        controller.run()

        
        mock_view.return_value.display_message.assert_called_once_with(
            "No hay rankings disponibles. Juega una partida para aparecer aquí."
        )

    @patch("controller.gameController.View")
    @patch("controller.gameController.Board")
    @patch("controller.gameController.DatabaseManager")
    def test_play_game_discover_bomb(self, mock_database_manager, mock_board, mock_view):
        
        mock_view.return_value.get_player_name.return_value = "TestPlayer"
        mock_view.return_value.display_difficulty_menu.return_value = 1
        mock_view.return_value.get_coordinates.return_value = (0, 0)
        mock_board.return_value.size = 6
        mock_board.return_value.tiles = [[MagicMock(is_bomb=True) for _ in range(6)] for _ in range(6)]
        mock_board.return_value.is_game_lost = True
        mock_database_manager.return_value.insert_player.return_value = True

        
        controller = GameController()
        controller.start_game()

        
        mock_view.return_value.display_message.assert_any_call("¡Has descubierto una bomba! +10 puntos.")
        mock_view.return_value.display_message.assert_any_call("¡Boom! Has perdido.")
        mock_database_manager.return_value.insert_player.assert_called_once_with("TestPlayer", 10)

    @patch("controller.gameController.View")
    @patch("controller.gameController.Board")
    @patch("controller.gameController.DatabaseManager")
    def test_play_game_win(self, mock_database_manager, mock_board, mock_view):
        
        mock_view.return_value.get_player_name.return_value = "TestPlayer"
        mock_view.return_value.display_difficulty_menu.return_value = 1
        mock_view.return_value.get_coordinates.return_value = (0, 0)
        mock_board.return_value.size = 6
        mock_board.return_value.tiles = [[MagicMock(is_bomb=False) for _ in range(6)] for _ in range(6)]
        mock_board.return_value.is_game_won.return_value = True
        mock_board.return_value.is_game_lost = False
        mock_database_manager.return_value.insert_player.return_value = True

        
        controller = GameController()
        controller.start_game()

        
        mock_view.return_value.display_message.assert_any_call("¡Felicidades! Has ganado con 0 puntos.")
        mock_database_manager.return_value.insert_player.assert_called_once_with("TestPlayer", 0)


if __name__ == "__main__":
    unittest.main()
