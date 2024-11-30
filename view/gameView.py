class View:
    def display_menu(self):
        """Muestra el menú principal."""
        print("\n=== Buscaminas ===")
        print("1. Jugar")
        print("2. Ver Rankings")
        print("3. Salir")
        return input("Selecciona una opción: ")

    def get_player_name(self):
        """Solicita el nombre del jugador."""
        return input("Introduce tu nombre: ")

    def display_difficulty_menu(self):
        """Muestra el menú de selección de dificultad."""
        while True:
            try:
                print("\nSelecciona la dificultad:")
                print("1. Fácil (6x6, 8 bombas)")
                print("2. Medio (8x8, 16 bombas)")
                print("3. Difícil (10x10, 32 bombas)")
                return int(input("Elige una opción (1-3): "))
            except ValueError:
                print("Opción no válida. Intenta de nuevo.")

    def display_board(self, board):
        """Muestra el tablero en consola con alineación adecuada."""
        # Encabezado con números de columna
        print("\n    " + " ".join([f"{col+1:2}" for col in range(board.size)]))
        print("   " + "-" * (board.size * 3 + 1))  # Línea separadora
        for idx, row in enumerate(board.tiles):
            # Fila con el número de fila y las casillas alineadas
            print(f"{idx+1:2} | " + " ".join(f"{tile.display():2}" for tile in row))
        print()

    def get_coordinates(self, board_size):
        """Solicita las coordenadas del jugador."""
        coords = input(f"Introduce las coordenadas (fila columna) [1-{board_size}]: ")
        x, y = map(int, coords.split())
        return x - 1, y - 1

    def display_message(self, message):
        """Muestra un mensaje al jugador."""
        print(message)

    def display_rankings(self, rankings):
        """Muestra los rankings."""
        print("\n=== Rankings ===")
        for rank, player in enumerate(rankings, start=1):
            print(f"{rank}. {player[1]} - {player[2]} puntos")
