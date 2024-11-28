import unittest
from unittest.mock import patch, MagicMock
from controller.gameController import GameController


class TestGameController(unittest.TestCase):
    @patch("controller.gameController.View")
    @patch("controller.gameController.Board")
    @patch("controller.gameController.DatabaseManager")
    def test_start_game(self, mock_database_manager, mock_board, mock_view):
        mock_view.return_value.display_menu.side_effect = ["1", "3"]
        mock_view.return_value.get_player_name.return_value = "TestPlayer"
        mock_view.return_value.display_difficulty_menu.return_value = 1
        mock_view.return_value.get_coordinates.side_effect = [(0, 0), (1, 1)]
        mock_board.return_value.size = 6
        mock_board.return_value.tiles = [[MagicMock(is_bomb=False) for _ in range(6)] for _ in range(6)]
        mock_board.return_value.is_game_won.side_effect = [False, True]
        mock_board.return_value.is_game_lost = False
        mock_board.return_value.total_bombs = 0
        mock_database_manager.return_value.insert_player.return_value = True

        controller = GameController()
        controller.run()

        mock_database_manager.return_value.insert_player.assert_called_once_with("TestPlayer", 100)

    @patch("controller.gameController.View")
    @patch("controller.gameController.DatabaseManager")
    def test_show_rankings_no_data(self, mock_database_manager, mock_view):
        mock_view.return_value.display_menu.side_effect = ["2", "3"]
        mock_database_manager.return_value.get_top_players.return_value = []

        controller = GameController()
        controller.run()

        mock_view.return_value.display_message.assert_any_call(
            "No hay rankings disponibles. Juega una partida para aparecer aquí."
        )

    @patch("controller.gameController.View")
    @patch("controller.gameController.Board")
    @patch("controller.gameController.DatabaseManager")
    def test_play_game_discover_bomb(self, mock_database_manager, mock_board, mock_view):
        
        mock_view.return_value.display_menu.side_effect = ["1", "3"]  
        mock_view.return_value.get_player_name.return_value = "TestPlayer"  
        mock_view.return_value.display_difficulty_menu.return_value = 1 
        mock_view.return_value.get_coordinates.return_value = (0, 0)  

        
        mock_board.return_value.size = 6
        mock_board.return_value.tiles = [[MagicMock(is_bomb=True) for _ in range(6)] for _ in range(6)]

        
        mock_board.return_value.is_game_lost = False
        mock_board.return_value.is_game_won.return_value = False

        
        def reveal_tile_effect(x, y):
            mock_board.return_value.is_game_lost = True  
            return None  

        mock_board.return_value.reveal_tile.side_effect = reveal_tile_effect

        
        mock_database_manager.return_value.insert_player.return_value = True

        
        controller = GameController()
        controller.run()

        
        mock_view.return_value.display_message.assert_any_call("¡Has descubierto una bomba! +10 puntos.")
        mock_view.return_value.display_message.assert_any_call("¡Boom! Has perdido. Puntos totales: 10")

        
        mock_database_manager.return_value.insert_player.assert_called_once_with("TestPlayer", 10)




    @patch("controller.gameController.View")
    @patch("controller.gameController.Board")
    @patch("controller.gameController.DatabaseManager")
    def test_play_game_win(self, mock_database_manager, mock_board, mock_view):
        mock_view.return_value.display_menu.side_effect = ["1", "3"]
        mock_view.return_value.get_player_name.return_value = "TestPlayer"
        mock_view.return_value.display_difficulty_menu.return_value = 1
        mock_view.return_value.get_coordinates.side_effect = [(0, 0), (1, 1)]
        mock_board.return_value.size = 6
        mock_board.return_value.tiles = [[MagicMock(is_bomb=False) for _ in range(6)] for _ in range(6)]
        mock_board.return_value.is_game_won.side_effect = [False, True]
        mock_board.return_value.is_game_lost = False
        mock_board.return_value.total_bombs = 0
        mock_database_manager.return_value.insert_player.return_value = True

        controller = GameController()
        controller.run()

        mock_view.return_value.display_message.assert_any_call("¡Felicidades! Has ganado con 100 puntos.")
        mock_database_manager.return_value.insert_player.assert_called_once_with("TestPlayer", 100)


if __name__ == "__main__":
    unittest.main()
