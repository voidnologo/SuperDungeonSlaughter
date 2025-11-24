import unittest
from unittest.mock import Mock, patch

from src.models.monster import Monster, MonsterData


class MonsterDataTests(unittest.TestCase):
    def test_monster_data_creation(self):
        data = MonsterData(
            name='Goblin', min_level=0, max_level=5, avg_hp=5, hp_sigma=0.5, damage_base=2, damage_sigma=1
        )
        self.assertEqual('Goblin', data.name)
        self.assertEqual(0, data.min_level)
        self.assertEqual(5, data.max_level)
        self.assertEqual(5, data.avg_hp)
        self.assertEqual(0.5, data.hp_sigma)
        self.assertEqual(2, data.damage_base)
        self.assertEqual(1, data.damage_sigma)

    def test_monster_data_is_frozen(self):
        data = MonsterData(name='Orc', min_level=2, max_level=8, avg_hp=7, hp_sigma=2, damage_base=3, damage_sigma=2)
        with self.assertRaises(AttributeError):
            data.avg_hp = 10

    def test_monster_data_validation_rejects_negative_min_level(self):
        with self.assertRaises(ValueError) as ctx:
            MonsterData(name='Bad', min_level=-1, max_level=5, avg_hp=5, hp_sigma=1, damage_base=2, damage_sigma=1)
        self.assertIn('min_level cannot be negative', str(ctx.exception))

    def test_monster_data_validation_rejects_max_level_less_than_min(self):
        with self.assertRaises(ValueError) as ctx:
            MonsterData(name='Bad', min_level=5, max_level=3, avg_hp=5, hp_sigma=1, damage_base=2, damage_sigma=1)
        self.assertIn('max_level must be > min_level', str(ctx.exception))

    def test_monster_data_validation_rejects_negative_hp(self):
        with self.assertRaises(ValueError) as ctx:
            MonsterData(name='Bad', min_level=0, max_level=5, avg_hp=-1, hp_sigma=1, damage_base=2, damage_sigma=1)
        self.assertIn('avg_hp must be positive', str(ctx.exception))

    def test_monster_data_validation_rejects_negative_damage(self):
        with self.assertRaises(ValueError) as ctx:
            MonsterData(name='Bad', min_level=0, max_level=5, avg_hp=5, hp_sigma=1, damage_base=-2, damage_sigma=1)
        self.assertIn('damage_base cannot be negative', str(ctx.exception))


class MonsterTests(unittest.TestCase):
    def setUp(self):
        self.monster = Monster(name='Slime', hp=5, hp_max=5, damage_base=2, damage_sigma=1)

    def test_monster_initialization(self):
        self.assertEqual('Slime', self.monster.name)
        self.assertEqual(5, self.monster.hp)
        self.assertEqual(5, self.monster.hp_max)
        self.assertEqual(2, self.monster.damage_base)
        self.assertEqual(1, self.monster.damage_sigma)

    @patch('src.models.monster.random.gauss', return_value=5.3)
    def test_monster_from_template(self, mock_gauss):
        template = MonsterData(
            name='Drake', min_level=3, max_level=10, avg_hp=9, hp_sigma=3, damage_base=3, damage_sigma=2
        )
        monster = Monster.from_template(template)

        self.assertEqual('Drake', monster.name)
        self.assertEqual(5, monster.hp)
        self.assertEqual(5, monster.hp_max)
        self.assertEqual(3, monster.damage_base)
        self.assertEqual(2, monster.damage_sigma)
        mock_gauss.assert_called_once_with(9, 3)

    @patch('src.models.monster.random.gauss', return_value=0.5)
    def test_monster_from_template_ensures_minimum_hp(self, mock_gauss):
        template = MonsterData(
            name='Weak', min_level=0, max_level=2, avg_hp=2, hp_sigma=2, damage_base=1, damage_sigma=0.5
        )
        monster = Monster.from_template(template)

        self.assertEqual(1, monster.hp)

    @patch('src.models.monster.random.gauss', return_value=3)
    def test_attack_deals_damage_to_opponent(self, mock_gauss):
        opponent = Mock()
        opponent.name = 'Hero'

        self.monster.attack(opponent)

        mock_gauss.assert_called_once_with(2, 1)
        opponent.take_damage.assert_called_once_with(3)

    @patch('src.models.monster.random.gauss', return_value=-2)
    def test_attack_clamps_negative_damage_to_zero(self, mock_gauss):
        opponent = Mock()
        opponent.name = 'Hero'

        self.monster.attack(opponent)

        opponent.take_damage.assert_called_once_with(0)

    def test_take_damage_reduces_hp(self):
        self.monster.take_damage(3)
        self.assertEqual(2, self.monster.hp)

    def test_take_damage_cannot_go_below_zero(self):
        self.monster.take_damage(10)
        self.assertEqual(0, self.monster.hp)

    def test_monster_str_representation(self):
        result = str(self.monster)
        expected = 'Slime HP> 5/5 BaseDmg> 2 DmgSigma> 1'
        self.assertEqual(expected, result)
