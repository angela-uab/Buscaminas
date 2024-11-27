import random
from model.tile import Tile


class Board:
    DIFFICULTY_SETTINGS = {
        1: {"size": 6, "bombs": 8},
        2: {"size": 8, "bombs": 16},
        3: {"size": 10, "bombs": 32},
    }

    def __init__(self, difficulty):
        if difficulty not in self.DIFFICULTY_SETTINGS:
            raise ValueError("Please choose 1, 2, or 3.")
        
        self.size = self.DIFFICULTY_SETTINGS[difficulty]["size"]
        self.total_bombs = self.DIFFICULTY_SETTINGS[difficulty]["bombs"]
        self.tiles = self._initialize_board()
        self.is_game_lost = False

    def _initialize_board(self):
        tiles = [[Tile() for _ in range(self.size)] for _ in range(self.size)]
        bomb_positions = random.sample(range(self.size * self.size), self.total_bombs)

        for pos in bomb_positions:
            row, col = divmod(pos, self.size)
            tiles[row][col].is_bomb = True

        for x in range(self.size):
            for y in range(self.size):
                tiles[x][y].neighboring_bombs = self._count_neighboring_bombs(tiles, x, y)

        return tiles

    def _count_neighboring_bombs(self, tiles, x, y):
        count = 0
        for i in range(max(0, x - 1), min(self.size, x + 2)):
            for j in range(max(0, y - 1), min(self.size, y + 2)):
                if tiles[i][j].is_bomb:
                    count += 1
        return count

    def reveal_tile(self, x, y):
        if self.tiles[x][y].is_bomb:
            self.is_game_lost = True
        self.tiles[x][y].reveal()

    def is_game_won(self):
        for row in self.tiles:
            for tile in row:
                if not tile.is_bomb and not tile.is_revealed:
                    return False
        return True

    def display_board(self):
        for row in self.tiles:
            print(" ".join(tile.display() for tile in row))
