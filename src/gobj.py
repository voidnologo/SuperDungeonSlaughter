from bestiary import Bestiary
from hero import Hero
from utils import ask_question


class Game():

    def __init__(self, hero=None):
        self.bestiary = Bestiary()
        self.hero = hero if hero else self.create_hero()
        self.monster = self.bestiary.get_a_monster_for_level(self.hero.level)

    def create_hero(self):
        name = ask_question("What is your hero's name?'")
        return Hero(name)
