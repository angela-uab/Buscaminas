import unittest
from model.player import Player

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(1, "Alice", 10)

    # Statement Coverage: Verifica que todas las sentencias del constructor se ejecuten correctamente.
    def test_initialization(self):
        self.assertEqual(self.player.get_id(), 1)
        self.assertEqual(self.player.get_name(), "Alice")
        self.assertEqual(self.player.get_score(), 10)

    # Partición Equivalente y Valores Límite para `set_id`
    def test_set_valid_id(self):
        self.player.set_id(0)  # Límite inferior válido
        self.assertEqual(self.player.get_id(), 0)
        self.player.set_id(100)  # Partición válida
        self.assertEqual(self.player.get_id(), 100)

    def test_set_invalid_id(self):
        with self.assertRaises(ValueError):  # Tipo inválido
            self.player.set_id("invalid_id")
        with self.assertRaises(ValueError):  # Valor negativo
            self.player.set_id(-1)

    # Partición Equivalente y Valores Límite para `set_name`
    def test_set_valid_name(self):
        self.player.set_name("Bob")  # Caso válido
        self.assertEqual(self.player.get_name(), "Bob")
        self.player.set_name("   John   ")  # Nombre con espacios
        self.assertEqual(self.player.get_name(), "   John   ")

    def test_set_invalid_name(self):
        with self.assertRaises(ValueError):  # Nombre vacío
            self.player.set_name("")
        with self.assertRaises(ValueError):  # Tipo inválido
            self.player.set_name(123)
        with self.assertRaises(ValueError):  # Nombre solo espacios
            self.player.set_name("   ")

    # Partición Equivalente y Valores Límite para `set_score`
    def test_set_valid_score(self):
        self.player.set_score(0)  # Límite inferior válido
        self.assertEqual(self.player.get_score(), 0)
        self.player.set_score(99.99)  # Partición válida (flotante)
        self.assertEqual(self.player.get_score(), 99.99)

    def test_set_invalid_score(self):
        with self.assertRaises(ValueError):  # Tipo inválido
            self.player.set_score("invalid_score")
        with self.assertRaises(ValueError):  # Valor negativo
            self.player.set_score(-10)

    # Path Coverage: Flujo completo al intentar asignar un nombre inválido
    def test_get_name_after_invalid_set(self):
        with self.assertRaises(ValueError):
            self.player.set_name("")
        self.assertEqual(self.player.get_name(), "Alice")  # Asegura que el estado previo se conserva

    # Path Coverage: Configurar puntaje en límites
    def test_set_score_limit(self):
        self.player.set_score(0)  # Límite inferior
        self.assertEqual(self.player.get_score(), 0)
        self.player.set_score(1000)  # Límite superior válido
        self.assertEqual(self.player.get_score(), 1000)

    # Decision Coverage: Combinaciones válidas e inválidas para ID
    def test_set_id_combinations(self):
        self.player.set_id(5)  # Caso válido
        self.assertEqual(self.player.get_id(), 5)
        with self.assertRaises(ValueError):  # Tipo inválido
            self.player.set_id("invalid_id")

    # Pruebas adicionales para el constructor
    def test_constructor_valid(self):
        player = Player(0, "Bob", 0)  # Valores válidos
        self.assertEqual(player.get_id(), 0)
        self.assertEqual(player.get_name(), "Bob")
        self.assertEqual(player.get_score(), 0)

    def test_constructor_invalid(self):
        with self.assertRaises(ValueError):  # ID inválido
            Player(-1, "Alice", 10)
        with self.assertRaises(ValueError):  # Nombre inválido
            Player(1, "", 10)
        with self.assertRaises(ValueError):  # Score inválido
            Player(1, "Alice", -10)

if __name__ == "__main__":
    unittest.main()
