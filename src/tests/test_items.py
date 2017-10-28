import unittest

from item import Item


class ItemsTests(unittest.TestCase):

    def test_get_item_fetches_correct_item(self):
        item = Item.get_item('sword')
        self.assertEqual(item.name, 'sword')
        self.assertEqual(item.description, 'Glistening, razor sharp sword')
        self.assertEqual(item.category, 'weapon')
        self.assertEqual(item.effect, 'hero:damage_min>+10%;damage_max>+10%')

    def test_apply_effect_updates_hero_stats(self):
        hero = Hero("Froto")
        game = Game(hero=hero)
        item = Item.get_item('sword')
