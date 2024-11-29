import pytest
from model.player import Player

import unittest

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player(1, "Alice", 10)

    # Statement Coverage: Verifica que todas las sentencias del constructor se ejecuten correctamente.
    def test_initialization(self):
        self.assertEqual(self.player.get_id(), 1)
        self.assertEqual(self.player.get_name(), "Alice")
        self.assertEqual(self.player.get_score(), 10)

    # Partición Equivalente: Verifica un caso válido para el ID.
    def test_set_id_valid(self):
        self.player.set_id(2)
        self.assertEqual(self.player.get_id(), 2)

    # Partición Equivalente y Valores Límite: Verifica que un tipo no válido (string) lanza un error.
    def test_set_invalid_id_type(self):
        with self.assertRaises(ValueError):
            self.player.set_id("invalid_id")

    # Valores Límite: Verifica que un valor fuera del rango permitido (negativo) lanza un error.
    def test_set_invalid_id_negative(self):
        with self.assertRaises(ValueError):
            self.player.set_id(-1)

    # Partición Equivalente: Verifica un caso válido para el nombre.
    def test_set_name_valid(self):
        self.player.set_name("Bob")
        self.assertEqual(self.player.get_name(), "Bob")

    # Partición Equivalente: Verifica que un tipo no válido para el nombre (e.g., número) lanza un error.
    def test_set_invalid_name_type(self):
        with self.assertRaises(ValueError):
            self.player.set_name(123)

    # Valores Límite: Verifica que un nombre vacío no puede ser asignado.
    def test_set_invalid_name_empty(self):
        with self.assertRaises(ValueError):
            self.player.set_name("")

    # Partición Equivalente: Verifica un caso válido para el puntaje.
    def test_set_score_valid(self):
        self.player.set_score(50)
        self.assertEqual(self.player.get_score(), 50)

    # Partición Equivalente: Verifica que un tipo no válido para el puntaje (e.g., string) lanza un error.
    def test_set_invalid_score_type(self):
        with self.assertRaises(ValueError):
            self.player.set_score("invalid_score")

    # Valores Límite: Verifica que un puntaje negativo no puede ser asignado.
    def test_set_invalid_score_negative(self):
        with self.assertRaises(ValueError):
            self.player.set_score(-10)

     # Path Coverage: Verifica el flujo de ejecución cuando se lanza un error al intentar asignar un nombre inválido.
    def test_get_name_after_invalid_set(self):
        with self.assertRaises(ValueError):
            self.player.set_name("")
        self.assertEqual(self.player.get_name(), "Alice")  
    
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

if __name__ == '__main__':
    unittest.main()
