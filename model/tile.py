class Tile:
    def __init__(self):
        self._is_bomb = False
        self._is_revealed = False
        self._neighboring_bombs = 0

        # Invariante: neighboring_bombs no puede ser negativo
        self._check_invariants()

    @property
    def is_bomb(self):
        return self._is_bomb

    @is_bomb.setter
    def is_bomb(self, value):
        # Precondición: value debe ser un booleano
        if not isinstance(value, bool):
            raise ValueError("is_bomb debe ser un booleano")
        self._is_bomb = value
        self._check_invariants()

    @property
    def is_revealed(self):
        return self._is_revealed
    
    @is_revealed.setter
    def is_revealed(self, value):
        # Precondición: value debe ser un booleano
        if not isinstance(value, bool):
            raise ValueError("is_revealed debe ser un booleano")
        self._is_revealed = value
        self._check_invariants()

    def reveal(self):
        # Precondición: El Tile no debe estar ya revelado
        if self._is_revealed:
            raise ValueError("El Tile ya está revelado")
        self._is_revealed = True
        # Postcondición: Después de revelar, is_revealed debe ser True
        assert self._is_revealed, "Error: El Tile no se marcó como revelado"

    @property
    def neighboring_bombs(self):
        return self._neighboring_bombs

    @neighboring_bombs.setter
    def neighboring_bombs(self, value):
        # Precondición: value debe ser un entero no negativo
        if not isinstance(value, int) or value < 0:
            raise ValueError("neighboring_bombs debe ser un entero no negativo")
        self._neighboring_bombs = value
        self._check_invariants()

    def display(self):
        # Invariante: neighboring_bombs debe estar definido
        assert self._neighboring_bombs >= 0, "Error: neighboring_bombs no válido"
        if self.is_revealed:
            return "X" if self.is_bomb else str(self.neighboring_bombs)
        return " "

    def _check_invariants(self):
        # Invariante: neighboring_bombs no puede ser negativo
        if self._neighboring_bombs < 0:
            raise ValueError("neighboring_bombs no puede ser negativo")
