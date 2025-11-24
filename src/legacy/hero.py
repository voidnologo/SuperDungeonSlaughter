import math
import random


class Hero:
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.hp_max = 10
        self.hp = 10
        self.damage_min = 0
        self.damage_max = 3
        self.total_kills = 0
        self.level_kills = 0
        self.heal_min = 1
        self.heal_max = 4

    def attack(self, opponent):
        damage = random.randint(self.damage_min, self.damage_max)
        opponent.hp -= damage
        print(f'{self.name} deals {damage} damage to the {opponent.name}!')

    def rest(self):
        heal = int(random.randint(self.heal_min, self.heal_max))
        self.hp += heal
        if self.hp > self.hp_max:
            self.hp = self.hp_max
        print(f'{self.name} heals {heal} damage!')

    def level_up(self):
        if not self.level_kills % self.level:
            self.level += 1
            self.hp_max += self.level
            self.level_kills = 0
            self.damage_min += 1 if self.damage_min == 0 else int(math.ceil(self.damage_min * 0.1))
            self.damage_max += 1 if self.damage_max == 0 else int(math.ceil(self.damage_max * 0.1))
            self.heal_min += 1 if self.heal_min == 0 else int(math.ceil(self.heal_min * 0.15))
            self.heal_max += 1 if self.heal_max == 0 else int(math.ceil(self.heal_max * 0.15))
            print('\nYou gained a level!\n')
            print(f'\t You are now level: {self.level}')
            print(f'\t You now have {self.hp_max} max hp.')
            print(f'\t You deal {self.damage_min} - {self.damage_max} points of damage.')
            print(f'\t You heal {self.heal_min} - {self.heal_max} when resting.')

    def __str__(self):
        return f'{self.name} - lvl {self.level}: HP> {self.hp} MaxHP> {self.hp_max} MinDmg> {self.damage_min} MaxDmg> {self.damage_max} MinHeal> {self.heal_min} MaxHeal> {self.heal_max} TotalKills> {self.total_kills}'
