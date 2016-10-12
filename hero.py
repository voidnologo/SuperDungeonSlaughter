import math
import random


class Hero():

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
        print('{} deals {} damage to the {}!'.format(self.name, damage, opponent.name))

    def rest(self):
        heal = int(random.randint(self.heal_min, self.heal_max))
        self.hp += heal
        if self.hp > self.hp_max:
            self.hp = self.hp_max
        print('{} heals {} damage!'.format(self.name, heal))

    def level_up(self):
        if (not self.level_kills % self.level):
            self.level += 1
            self.hp_max += self.level
            self.level_kills = 0
            self.damage_min += 1 if self.damage_min == 0 else int(math.ceil(self.damage_min * 0.1))
            self.damage_max += 1 if self.damage_max == 0 else int(math.ceil(self.damage_max * 0.1))
            self.heal_min += 1 if self.heal_min == 0 else int(math.ceil(self.heal_min * 0.1))
            self.heal_max += 1 if self.heal_max == 0 else int(math.ceil(self.heal_max * 0.1))
            print("\nYou gained a level!\n")
            print("\t You are now level: {}".format(self.level))
            print("\t You now have {} max hp.".format(self.hp_max))
            print("\t You deal {} - {} points of damage.".format(self.damage_min, self.damage_max))
            print("\t You heal {} - {} when resting.".format(self.heal_min, self.heal_max))

    def __str__(self):
        return '{} - lvl {}: HP> {} MaxHP> {} MinDmg> {} MaxDmg> {} MinHeal> {} MaxHeal> {} TotalKills> {}'.format(
            self.name, self.level, self.hp, self.hp_max, self.damage_min, self.damage_max, self.heal_min,
            self.heal_max, self.total_kills
        )
