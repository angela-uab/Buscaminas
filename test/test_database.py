import unittest
from model.database_manager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configura la base de datos de prueba antes de todos los tests."""
        cls.test_db_file = "test_database.db"
        cls.db = DatabaseManager(cls.test_db_file)

    def setUp(self):
        """Limpia la base de datos antes de cada test."""
        self.db.connection.execute("DELETE FROM players")
        self.db.connection.commit()

    @classmethod
    def tearDownClass(cls):
        """Cierra la conexión después de todos los tests."""
        cls.db.close()

    # Partición Equivalente: Verifica entradas inválidas para insertar un jugador.
    def test_invalid_insert_player(self):
        with self.assertRaises(ValueError):
            self.db.insert_player("", 10)  # Nombre vacío no permitido
        with self.assertRaises(ValueError):
            self.db.insert_player(None, 10)  # Nombre None no permitido
        with self.assertRaises(ValueError):
            self.db.insert_player("Alice", "invalid_score")  # Puntaje debe ser un número
        with self.assertRaises(ValueError):
            self.db.insert_player("Alice", -1)  # Puntaje negativo no permitido

    # Statement Coverage: Verifica manejo de errores al buscar un jugador con ID inválido.
    def test_invalid_get_player_by_id(self):
        player_id = self.db.insert_player("Alice", 10)  # Insertamos un jugador válido
        self.assertIsNotNone(player_id, "El jugador no fue insertado correctamente.")
        
        with self.assertRaises(ValueError):
            self.db.get_player_by_id("invalid_id")  # ID no es un entero
        player = self.db.get_player_by_id(999)  # ID inexistente
        self.assertIsNone(player)

    # Statement Coverage: Verifica manejo de errores al eliminar un jugador con ID inválido.
    def test_invalid_delete_player(self):
        player_id = self.db.insert_player("Alice", 10)  # Insertamos un jugador válido
        self.assertIsNotNone(player_id, "El jugador no fue insertado correctamente.")
        
        with self.assertRaises(ValueError):
            self.db.delete_player("invalid_id")  # ID no es un entero
        result = self.db.delete_player(999)  # ID inexistente
        self.assertFalse(result, "Se esperaba que no se eliminara ninguna fila para un ID inexistente.")

    # Path Coverage: Verifica la inserción de múltiples jugadores y su recuperación.
    def test_insert_two_players(self):
        result_alice = self.db.insert_player("Alice", 10)
        result_bob = self.db.insert_player("Bob", 25)
        
        self.assertIsNotNone(result_alice, "El jugador 'Alice' no fue insertado correctamente.")
        self.assertIsNotNone(result_bob, "El jugador 'Bob' no fue insertado correctamente.")

        players = self.db.get_all_players()
        self.assertEqual(len(players), 2)
        self.assertEqual(players[0][1], "Alice")
        self.assertEqual(players[0][2], 10)
        self.assertEqual(players[1][1], "Bob")
        self.assertEqual(players[1][2], 25)

    # Path Coverage: Verifica el flujo de inserción y eliminación de jugadores.
    def test_delete_player(self):
        player_id_alice = self.db.insert_player("Alice", 10)
        player_id_bob = self.db.insert_player("Bob", 25)

        self.assertIsNotNone(player_id_alice, "El jugador 'Alice' no fue insertado correctamente.")
        self.assertIsNotNone(player_id_bob, "El jugador 'Bob' no fue insertado correctamente.")

        result = self.db.delete_player(player_id_alice)
        self.assertTrue(result, "El jugador 'Alice' no fue eliminado correctamente.")

        players = self.db.get_all_players()
        self.assertEqual(len(players), 1)
        self.assertEqual(players[0][1], "Bob")

    # Decision Coverage: Verifica búsqueda correcta de un jugador por ID.
    def test_get_player_by_id(self):
        player_id = self.db.insert_player("Alice", 10)
        self.assertIsNotNone(player_id, "El jugador no fue insertado correctamente.")

        player = self.db.get_player_by_id(player_id)
        self.assertIsNotNone(player, f"No se encontró el jugador con ID {player_id}.")
        self.assertEqual(player[1], "Alice")
        self.assertEqual(player[2], 10)

    # Path Coverage: Verifica la actualización de puntaje para un jugador existente.
    def test_update_player_score(self):
        player_id = self.db.insert_player("Alice", 10)
        self.assertIsNotNone(player_id, "El jugador no fue insertado correctamente.")

        result = self.db.update_player_score(player_id, 50)
        self.assertTrue(result, f"No se pudo actualizar el puntaje del jugador con ID {player_id}.")

        player = self.db.get_player_by_id(player_id)
        self.assertIsNotNone(player, f"No se encontró el jugador con ID {player_id} tras actualizar la puntuación.")
        self.assertEqual(player[2], 50)

    # Partición Equivalente y Loop Testing: Verifica recuperación de los mejores puntajes.
    def test_get_top_players(self):
        self.db.insert_player("Alice", 10)
        self.db.insert_player("Bob", 25)
        self.db.insert_player("Charlie", 15)

        top_players = self.db.get_top_players(2)
        self.assertEqual(len(top_players), 2)
        self.assertEqual(top_players[0][1], "Bob")  # Mejor puntuación
        self.assertEqual(top_players[1][1], "Charlie")  # Segunda mejor puntuación

    def test_get_top_players_limit_cases(self):
        # Caso 1: Base de datos vacía
        top_players = self.db.get_top_players(1)
        self.assertEqual(len(top_players), 0)

        # Caso 2: Límite igual a 0
        with self.assertRaises(ValueError):  # Límite no puede ser 0
            self.db.get_top_players(0)

        # Caso 3: Límite mayor al número total de jugadores
        self.db.insert_player("Alice", 50)
        self.db.insert_player("Bob", 100)
        top_players = self.db.get_top_players(10)  # Más de los jugadores registrados
        self.assertEqual(len(top_players), 2)
        self.assertEqual(top_players[0][1], "Bob")  # Mayor puntaje
        self.assertEqual(top_players[1][1], "Alice")

        # Caso 4: Límite igual al número total de jugadores
        top_players = self.db.get_top_players(2)
        self.assertEqual(len(top_players), 2)
        self.assertEqual(top_players[0][1], "Bob")
        self.assertEqual(top_players[1][1], "Alice")

        # Caso 5: Límite igual a 1
        top_players = self.db.get_top_players(1)
        self.assertEqual(len(top_players), 1)
        self.assertEqual(top_players[0][1], "Bob")

        # Caso 6: Base de datos con un único jugador
        self.db = DatabaseManager()  # Reinicia la base de datos
        self.db.insert_player("Charlie", 70)
        top_players = self.db.get_top_players(1)
        self.assertEqual(len(top_players), 1)
        self.assertEqual(top_players[0][1], "Charlie")

        # Caso 7: Base de datos con jugadores con puntuaciones iguales
        self.db = DatabaseManager()  # Reinicia la base de datos
        self.db.insert_player("Dan", 90)
        self.db.insert_player("Eve", 90)
        top_players = self.db.get_top_players(2)
        self.assertEqual(len(top_players), 2)
        self.assertIn(top_players[0][1], ["Dan", "Eve"])  # Ambos tienen el mismo puntaje
        self.assertIn(top_players[1][1], ["Dan", "Eve"])


if __name__ == "__main__":
    unittest.main()
