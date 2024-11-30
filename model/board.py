import random
from model.tile import Tile

class Board:
    DIFFICULTY_SETTINGS = {
        1: {"size": 6, "bombs": 8},
        2: {"size": 8, "bombs": 16},
        3: {"size": 10, "bombs": 32},
    }

    def __init__(self, difficulty):
        # Precondición: La dificultad debe ser un valor válido (1, 2 o 3)
        if difficulty not in self.DIFFICULTY_SETTINGS:
            raise ValueError("La dificultad debe ser 1, 2 o 3.")
        
        # Inicialización
        self.size = self.DIFFICULTY_SETTINGS[difficulty]["size"]
        self.total_bombs = self.DIFFICULTY_SETTINGS[difficulty]["bombs"]
        self.tiles = self._initialize_board()
        self.is_game_lost = False

        # Invariante: El número total de bombas debe coincidir con la configuración
        self._check_invariants()

    def _initialize_board(self):
        # Inicializar el tablero y colocar las bombas
        tiles = [[Tile() for _ in range(self.size)] for _ in range(self.size)]
        bomb_positions = random.sample(range(self.size * self.size), self.total_bombs)

        for pos in bomb_positions:
            row, col = divmod(pos, self.size)
            tiles[row][col].is_bomb = True

        # Calcular las bombas vecinas para cada casilla
        for x in range(self.size):
            for y in range(self.size):
                tiles[x][y].neighboring_bombs = self._count_neighboring_bombs(tiles, x, y)

        # Postcondición: Asegurar que el número total de bombas en el tablero sea correcto
        total_bombs_counted = sum(tile.is_bomb for row in tiles for tile in row)
        assert total_bombs_counted == self.total_bombs, "Número de bombas en el tablero no coincide con la configuración."

        return tiles

    def _count_neighboring_bombs(self, tiles, x, y):
        # Precondiciones: Coordenadas válidas
        assert 0 <= x < self.size, f"x está fuera de rango: {x}"
        assert 0 <= y < self.size, f"y está fuera de rango: {y}"

        # Contar las bombas vecinas
        count = 0
        for i in range(max(0, x - 1), min(self.size, x + 2)):
            for j in range(max(0, y - 1), min(self.size, y + 2)):
                if tiles[i][j].is_bomb:
                    count += 1

        # Postcondición: El conteo de bombas debe ser un número no negativo
        assert count >= 0, "El conteo de bombas vecinas no puede ser negativo."
        return count

    def reveal_tile(self, x, y):
        # Precondiciones: Coordenadas válidas y casilla no revelada
        assert 0 <= x < self.size, f"x está fuera de rango: {x}"
        assert 0 <= y < self.size, f"y está fuera de rango: {y}"
        assert not self.tiles[x][y].is_revealed, "La casilla ya está revelada."

        # Revelar casilla
        if self.tiles[x][y].is_bomb:
            self.is_game_lost = True
        self.tiles[x][y].reveal()

        # Postcondición: La casilla debe estar marcada como revelada
        assert self.tiles[x][y].is_revealed, "La casilla no se marcó como revelada correctamente."

    def is_game_won(self):
        # Verificar si todas las casillas no bomba están reveladas
        for row in self.tiles:
            for tile in row:
                # Invariante: Una casilla que no es bomba y no está revelada indica que el juego no está ganado
                if not tile.is_bomb and not tile.is_revealed:
                    return False
        return True

    def display_board(self):
        # Invariante: La longitud de cada fila debe coincidir con el tamaño del tablero
        for row in self.tiles:
            assert len(row) == self.size, "El tamaño de la fila no coincide con el tamaño del tablero."
        # Mostrar el tablero
        for row in self.tiles:
            print(" ".join(tile.display() for tile in row))

    def _check_invariants(self):
        # Invariante: El tamaño debe ser consistente con las configuraciones
        assert self.size > 0, "El tamaño del tablero debe ser mayor que 0."
        assert self.total_bombs >= 0, "El número de bombas debe ser no negativo."

        # Invariante: Asegurar que el número total de bombas no excede el número total de casillas
        assert self.total_bombs <= self.size * self.size, "Número de bombas excede el número total de casillas."
