import unittest
from unittest.mock import Mock

from src.systems.combat import CombatEngine


class CombatEngineTests(unittest.TestCase):
    def setUp(self):
        self.engine = CombatEngine()
        self.attacker = Mock()
        self.defender = Mock()

    def test_execute_attack_calls_attacker_attack(self):
        self.engine.execute_attack(self.attacker, self.defender)
        self.attacker.attack.assert_called_once_with(self.defender)

    def test_is_defeated_returns_true_when_hp_is_zero(self):
        combatant = Mock()
        combatant.hp = 0
        self.assertTrue(self.engine.is_defeated(combatant))

    def test_is_defeated_returns_true_when_hp_is_negative(self):
        combatant = Mock()
        combatant.hp = -5
        self.assertTrue(self.engine.is_defeated(combatant))

    def test_is_defeated_returns_false_when_hp_is_positive(self):
        combatant = Mock()
        combatant.hp = 1
        self.assertFalse(self.engine.is_defeated(combatant))
