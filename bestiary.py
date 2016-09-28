from collections import defaultdict
import random
import simplejson as json

import gobj


def get_monster_data_from_file(file_name):
    with open(file_name, 'r') as f:
        return json.loads(f.read())


def monsters_by_level(data):
    by_levels = defaultdict(list)
    for creature in data:
        for level in range(data[creature]['min_level'], data[creature]['max_level']):
            by_levels[level].append(creature)
    return by_levels


def make_a_monster(name, data):
    hp = int(random.gauss(data['avg_hp'], data['hp_sigma']))
    if hp < 1:
        hp = 1
    return {
        'name': name,
        'hp': hp,
        'hp_max': hp,
        'damage_base': data['damage_base'],
        'damage_sigma': data['damage_sigma'],
    }


def get_a_monster_for_level(level):
    monster = random.choice(gobj.MONSTERS_BY_LEVEL[level])
    return make_a_monster(monster, gobj.MONSTER_DATA[monster])
