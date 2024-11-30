class Player:
    def __init__(self, player_id, name, score):
        # Precondiciones: Validar argumentos
        if not isinstance(player_id, int) or player_id < 0:
            raise ValueError("Player ID debe ser un entero no negativo.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("El nombre debe ser una cadena no vacía.")
        if not isinstance(score, (int, float)) or score < 0:
            raise ValueError("El puntaje debe ser un número no negativo.")
        
        # Asignación después de validar precondiciones
        self._id = player_id
        self._name = name
        self._score = score

        # Invariantes
        self._check_invariants()

    def get_id(self):
        # Invariante: El ID debe ser un entero no negativo
        assert isinstance(self._id, int) and self._id >= 0, "El ID debe ser un entero no negativo."
        return self._id

    def set_id(self, player_id):
        # Precondición: El ID debe ser un entero no negativo
        if not isinstance(player_id, int) or player_id < 0:
            raise ValueError("Player ID debe ser un entero no negativo.")
        
        # Asignación después de validar
        self._id = player_id

        # Postcondición: El nuevo ID debe coincidir con el valor asignado
        assert self._id == player_id, "El ID no fue correctamente asignado."

        # Invariantes
        self._check_invariants()

    def get_name(self):
        # Invariante: El nombre debe ser una cadena no vacía
        assert isinstance(self._name, str) and self._name.strip(), "El nombre debe ser una cadena no vacía."
        return self._name

    def set_name(self, name):
        # Precondición: El nombre debe ser una cadena no vacía
        if not isinstance(name, str) or not name.strip():
            raise ValueError("El nombre debe ser una cadena no vacía.")
        
        # Asignación después de validar
        self._name = name

        # Postcondición: El nuevo nombre debe coincidir con el valor asignado
        assert self._name == name, "El nombre no fue correctamente asignado."

        # Invariantes
        self._check_invariants()

    def get_score(self):
        # Invariante: El puntaje debe ser un número no negativo
        assert isinstance(self._score, (int, float)) and self._score >= 0, "El puntaje debe ser un número no negativo."
        return self._score

    def set_score(self, score):
        # Precondición: El puntaje debe ser un número no negativo
        if not isinstance(score, (int, float)) or score < 0:
            raise ValueError("El puntaje debe ser un número no negativo.")
        
        # Asignación después de validar
        self._score = score

        # Postcondición: El nuevo puntaje debe coincidir con el valor asignado
        assert self._score == score, "El puntaje no fue correctamente asignado."

        # Invariantes
        self._check_invariants()

    def _check_invariants(self):
        # Invariante: El ID debe ser un entero no negativo
        assert isinstance(self._id, int) and self._id >= 0, "El ID debe ser un entero no negativo."
        
        # Invariante: El nombre debe ser una cadena no vacía
        assert isinstance(self._name, str) and self._name.strip(), "El nombre debe ser una cadena no vacía."
        
        # Invariante: El puntaje debe ser un número no negativo
        assert isinstance(self._score, (int, float)) and self._score >= 0, "El puntaje debe ser un número no negativo."
