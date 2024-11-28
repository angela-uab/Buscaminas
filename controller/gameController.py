from model.board import Board
from model.database_manager import DatabaseManager
from model.player import Player
from view.gameView import View


class GameController:
    def __init__(self):
        self.view = View()
        self.database = DatabaseManager("database.db")

    def run(self):
        option = self.view.display_menu()
        if option == "1":
            self.start_game()
        elif option == "2":
            self.show_rankings()
        elif option == "3":
            self.view.display_message("¡Gracias por jugar!")

    def start_game(self):
        player_name = self.view.get_player_name()
        difficulty = self.view.display_difficulty_menu()
        board = Board(difficulty)
        player = Player(0, player_name, 0)
        self.play_game(board, player)

    def play_game(self, board, player):
        self.view.display_board(board)
        x, y = self.view.get_coordinates(board.size)
        board.reveal_tile(x, y)

        if board.tiles[x][y].is_bomb:
            player.set_score(player.get_score() + 10)
            self.view.display_message("¡Has descubierto una bomba! +10 puntos.")

        if board.is_game_lost:
            self.view.display_message("¡Boom! Has perdido.")
            self.database.insert_player(player.get_name(), player.get_score())
            return  # Detenemos el flujo para evitar verificar la victoria

        if board.is_game_won():
            self.view.display_message(f"¡Felicidades! Has ganado con {player.get_score()} puntos.")
            self.database.insert_player(player.get_name(), player.get_score())


    def show_rankings(self):
        rankings = self.database.get_top_players()
        if rankings:
            self.view.display_rankings(rankings)
        else:
            self.view.display_message("No hay rankings disponibles. Juega una partida para aparecer aquí.")
