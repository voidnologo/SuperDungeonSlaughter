import unittest
from unittest.mock import Mock, patch

from src.models.combatant import CombatStats
from src.models.hero import Hero


class HeroTests(unittest.TestCase):
    def setUp(self):
        self.hero = Hero(name='Froto')

    def test_hero_initialization(self):
        self.assertEqual('Froto', self.hero.name)
        self.assertEqual(1, self.hero.level)
        self.assertEqual(10, self.hero.hp)
        self.assertEqual(10, self.hero.hp_max)
        self.assertEqual(0, self.hero.total_kills)
        self.assertEqual(0, self.hero.level_kills)
        self.assertEqual(CombatStats(0, 3), self.hero.damage_stats)
        self.assertEqual(CombatStats(1, 4), self.hero.heal_stats)

    def test_hero_str_shows_stats(self):
        expected = 'Froto - lvl 1: HP> 10 MaxHP> 10 MinDmg> 0 MaxDmg> 3 MinHeal> 1 MaxHeal> 4 TotalKills> 0'
        self.assertEqual(expected, str(self.hero))

    def test_take_damage_reduces_hp(self):
        self.hero.take_damage(5)
        self.assertEqual(5, self.hero.hp)

    def test_take_damage_cannot_go_below_zero(self):
        self.hero.take_damage(20)
        self.assertEqual(0, self.hero.hp)

    @patch('src.models.hero.random.randint', return_value=2)
    def test_attack_deals_damage_to_opponent(self, mock_randint):
        opponent = Mock()
        opponent.name = 'Goblin'

        self.hero.attack(opponent)

        mock_randint.assert_called_once_with(0, 3)
        opponent.take_damage.assert_called_once_with(2)

    @patch('src.models.hero.random.randint', return_value=3)
    def test_rest_heals_hp(self, mock_randint):
        self.hero.hp = 5
        self.hero.rest()

        self.assertEqual(8, self.hero.hp)
        mock_randint.assert_called_once_with(1, 4)

    @patch('src.models.hero.random.randint', return_value=4)
    def test_rest_cannot_exceed_max_hp(self, mock_randint):
        self.hero.hp = 8
        self.hero.rest()

        self.assertEqual(10, self.hero.hp)

    def test_level_up_does_not_trigger_before_threshold(self):
        self.hero.level_kills = 0
        self.hero.level_up()

        self.assertEqual(1, self.hero.level)
        self.assertEqual(0, self.hero.level_kills)

    def test_level_up_triggers_at_threshold(self):
        self.hero.level_kills = 1

        with patch('builtins.print'):
            self.hero.level_up()

        self.assertEqual(2, self.hero.level)
        self.assertEqual(0, self.hero.level_kills)
        self.assertEqual(12, self.hero.hp_max)
        self.assertEqual(CombatStats(1, 4), self.hero.damage_stats)
        self.assertEqual(CombatStats(2, 5), self.hero.heal_stats)

    def test_level_up_at_level_2_requires_2_kills(self):
        self.hero.level = 2
        self.hero.level_kills = 1
        self.hero.level_up()

        self.assertEqual(2, self.hero.level)

        self.hero.level_kills = 2
        with patch('builtins.print'):
            self.hero.level_up()

        self.assertEqual(3, self.hero.level)

    def test_scale_stat_increases_by_percentage(self):
        result = self.hero._scale_stat(10, 0.1)
        self.assertEqual(11, result)

    def test_scale_stat_minimum_increase_of_one(self):
        result = self.hero._scale_stat(0, 0.1)
        self.assertEqual(1, result)
