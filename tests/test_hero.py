import unittest
from hero import Hero


class HeroTests(unittest.TestCase):

    def test_hero_str_shows_stats(self):
        hero = Hero("Froto")
        self.assertEqual(
            "Froto - lvl 1: HP> 10 MaxHP> 10 MinDmg> 0 MaxDmg> 3 MinHeal> 1 MaxHeal> 4 TotalKills> 0",
            str(hero)
        )
