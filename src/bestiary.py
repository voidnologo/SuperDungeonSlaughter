from collections import defaultdict
import random
import simplejson as json

from utils import data_file_path


class Bestiary():

    def __init__(self):
        fpath = data_file_path('monsters.json')
        self.bestiary = self.get_monster_data_from_file(fpath)
        self.level_groups = self.monsters_by_level()

    def get_monster_data_from_file(self, file_name):
        with open(file_name, 'r') as f:
            return json.loads(f.read())

    def monsters_by_level(self):
        by_levels = defaultdict(list)
        for creature in self.bestiary:
            for level in range(self.bestiary[creature]['min_level'], self.bestiary[creature]['max_level']):
                by_levels[level].append(creature)
        return by_levels

    def get_a_monster_for_level(self, level):
        monster = random.choice(self.level_groups[level])
        return Monster(monster, self.bestiary[monster])


class Monster():

    def __init__(self, name, data):
        hp = int(random.gauss(data['avg_hp'], data['hp_sigma']))
        self.name = name
        self.hp = hp if hp >= 1 else 1
        self.hp_max = self.hp
        self.damage_base = data['damage_base']
        self.damage_sigma = data['damage_sigma']

    def attack(self, opponent):
        damage = int(random.gauss(self.damage_base, self.damage_sigma))
        opponent.hp -= damage
        print('{} deals {} damage to {}!'.format(self.name, damage, opponent.name))

    def __str__(self):
        return '{} HP> {}/{} BaseDmg> {} DmgSigma> {}'.format(
            self.name, self.hp, self.hp_max, self.damage_base, self.damage_sigma
        )
