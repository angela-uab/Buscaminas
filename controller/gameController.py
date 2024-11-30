from model.board import Board
from model.database_manager import DatabaseManager
from model.player import Player
from view.gameView import View


class GameController:
    def __init__(self):
        """
        Inicializa el controlador del juego con vista y base de datos.
        """
        # Postcondición: La vista y la base de datos deben estar inicializadas.
        self.view = View()
        self.database = DatabaseManager("database.db")
        assert self.view is not None, "La vista no se inicializó correctamente."
        assert self.database is not None, "La base de datos no se inicializó correctamente."

    def run(self):
        """
        Controla el menú principal.
        """
        # Invariante: La vista debe estar lista para interactuar.
        assert self.view is not None, "La vista no está inicializada."
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
        """
        Inicia una partida.
        """
        # Precondición: La vista debe estar inicializada para recibir datos del jugador.
        assert self.view is not None, "La vista no está inicializada."
        player_name = self.view.get_player_name()
        difficulty = self.view.display_difficulty_menu()

        try:
            # Precondición: La dificultad debe ser válida (1, 2 o 3).
            board = Board(difficulty)
            player = Player(0, player_name, 0)

            # Postcondición: El jugador y el tablero deben estar inicializados correctamente.
            assert board is not None, "El tablero no se inicializó correctamente."
            assert player is not None, "El jugador no se inicializó correctamente."

            self.play_game(board, player)
        except ValueError:
            self.view.display_message("Dificultad no válida. Volviendo al menú principal...")

    def play_game(self, board, player):
        """
        Lógica principal del juego.
        """
        # Precondiciones
        assert board is not None, "El tablero no está inicializado."
        assert player is not None, "El jugador no está inicializado."

        while not board.is_game_won() and not board.is_game_lost:
            self.view.display_board(board)

            try:
                x, y = self.view.get_coordinates(board.size)

                # Precondición: Las coordenadas deben estar dentro del rango del tablero.
                assert 0 <= x < board.size, f"La coordenada x={x} está fuera de rango."
                assert 0 <= y < board.size, f"La coordenada y={y} está fuera de rango."

                # Revela la casilla seleccionada
                is_bomb = board.tiles[x][y].is_bomb
                board.reveal_tile(x, y)

                # Postcondición: La casilla debe estar revelada.
                assert board.tiles[x][y].is_revealed, "La casilla no se reveló correctamente."

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
        """
        Guarda el jugador en la base de datos.
        """
        # Precondición: El jugador debe tener un nombre y un puntaje válido.
        assert player.get_name(), "El jugador no tiene un nombre válido."
        assert player.get_score() >= 0, "El puntaje del jugador no es válido."

        success = self.database.insert_player(player.get_name(), player.get_score())

        # Postcondición: La operación debe ser exitosa o manejar el error adecuadamente.
        if success:
            self.view.display_message("¡Tu puntaje se ha guardado correctamente!")
        else:
            self.view.display_message("Hubo un error al guardar tu puntaje en la base de datos.")

    def show_rankings(self):
        """
        Muestra los rankings desde la base de datos.
        """
        # Invariante: La base de datos debe estar inicializada.
        assert self.database is not None, "La base de datos no está inicializada."

        rankings = self.database.get_top_players()

        # Postcondición: Los rankings deben ser una lista o estar vacíos.
        assert isinstance(rankings, list), "Los rankings no son válidos."

        if rankings:
            self.view.display_rankings(rankings)
        else:
            self.view.display_message("No hay rankings disponibles. Juega una partida para aparecer aquí.")
