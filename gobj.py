from bestiary import Bestiary
from hero import Hero
from utils import ask_question


class Game():

    def __init__(self):
        self.bestiary = Bestiary()
        name = ask_question("What is your hero's name?'")
        self.hero = Hero(name)
        self.monster = self.bestiary.get_a_monster_for_level(self.hero.level)
