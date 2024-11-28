from model.board import Board
from model.database_manager import DatabaseManager
from model.player import Player
from view.gameView import View


class GameController:
    def __init__(self):
        self.view = View()
        self.database = DatabaseManager("database.db")

    def run(self):
        """Controla el menú principal."""
        while True:
            option = self.view.display_menu()
            if option == "1":
                self.start_game()
            elif option == "2":
                self.show_rankings()
            elif option == "3":
                self.view.display_message("¡Gracias por jugar!")
                break
            else:
                self.view.display_message("Opción no válida. Intenta de nuevo.")

    def start_game(self):
        """Inicia una partida."""
        player_name = self.view.get_player_name()
        difficulty = self.view.display_difficulty_menu()

        try:
            board = Board(difficulty)
            player = Player(0, player_name, 0)
            self.play_game(board, player)
        except ValueError:
            self.view.display_message("Dificultad no válida. Volviendo al menú principal...")

    def play_game(self, board, player):
        """Lógica principal del juego."""
        while not board.is_game_won() and not board.is_game_lost:
            self.view.display_board(board)
            try:
                x, y = self.view.get_coordinates(board.size)
                # Revela la casilla seleccionada
                is_bomb = board.tiles[x][y].is_bomb
                board.reveal_tile(x, y)

                # Suma puntos si se descubre una bomba
                if is_bomb:
                    player.set_score(player.get_score() + 10)
                    self.view.display_message("¡Has descubierto una bomba! +10 puntos.")
            except (ValueError, IndexError):
                self.view.display_message("Coordenadas inválidas. Intenta de nuevo.")

        self.view.display_board(board)

        if board.is_game_lost:
            self.view.display_message(f"¡Boom! Has perdido. Puntos totales: {player.get_score()}")
            self.save_player_to_rankings(player)
        else:
            # Añade puntaje adicional al ganar
            player.set_score(player.get_score() + (100 - board.total_bombs))
            self.view.display_message(f"¡Felicidades! Has ganado con {player.get_score()} puntos.")
            self.save_player_to_rankings(player)

    def save_player_to_rankings(self, player):
        """Guarda el jugador en la base de datos."""
        success = self.database.insert_player(player.get_name(), player.get_score())
        if success:
            self.view.display_message("¡Tu puntaje se ha guardado correctamente!")
        else:
            self.view.display_message("Hubo un error al guardar tu puntaje en la base de datos.")

    def show_rankings(self):
        """Muestra los rankings desde la base de datos."""
        rankings = self.database.get_top_players()
        if rankings:
            self.view.display_rankings(rankings)
        else:
            self.view.display_message("No hay rankings disponibles. Juega una partida para aparecer aquí.")