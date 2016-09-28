import cmd
from bisect import bisect
import math
import random

from bestiary import get_monster_data_from_file, monsters_by_level, get_a_monster_for_level
from colors import bcolors
import gobj
from hero import initialize_hero


class GameLoop(cmd.Cmd):
    welcome = "{}{}{} Welcome to Super Dungeon Slaughter! {}\n\n".format(bcolors.BOLD, bcolors.UNDERLINE, bcolors.BG_RED, bcolors.ENDC)
    doc_header = 'Commands'
    undoc_header = 'No help available'
    ruler = '-'

    def preloop(self):
        print(self.welcome)
        self.initialize_game()

    def do_f(self, args):
        "Fight"
        self.do_fight(args)

    def do_fight(self, args):
        "Fight"
        hero_attack = random.randint(gobj.HERO['damage_min'], gobj.HERO['damage_max'])
        monster_attack = int(random.gauss(gobj.MONSTER['damage_base'], gobj.MONSTER['damage_sigma']))
        gobj.HERO['hp'] -= monster_attack
        gobj.MONSTER['hp'] -= hero_attack
        print('{} deals {} damage to the {}!'.format(gobj.HERO['name'], hero_attack, gobj.MONSTER['name']))
        print('The {} deals {} damage to {}!'.format(gobj.MONSTER['name'], monster_attack, gobj.HERO['name']))

    def do_r(self, args):
        "Rest"
        self.do_rest(args)

    def do_rest(self, args):
        "Rest"
        monster_attack = int(random.gauss(gobj.MONSTER['damage_base'], gobj.MONSTER['damage_sigma']))
        hero_heal = int(random.randint(gobj.HERO['heal_min'], gobj.HERO['heal_max']))
        gobj.HERO['hp'] += hero_heal
        if gobj.HERO['hp'] >= gobj.HERO['hp_max']:
            gobj.HERO['hp'] = gobj.HERO['hp_max']
        gobj.HERO['hp'] -= monster_attack
        print('{} heals {} damage!'.format(gobj.HERO['name'], hero_heal))
        print('The {} deals {} damage to {}!'.format(gobj.MONSTER['name'], monster_attack, gobj.HERO['name']))

    def do_escape(self, args):
        "Leave the game with your current score"
        print('escape')
        pass

    def do_quit(self, args):
        "Quit - lose everything!"
        print('quit')
        pass

    def do_look(self, args):
        print('look')
        pass
        # if args == 'room':

    def postcmd(self, stop, line):
        if self.hero_died():
            self.lose_game()
        if self.monster_died():
            self.level_up()

    def hero_died(self):
        if gobj.HERO['hp'] <= 0:
            return True
        return False

    def lose_game(self):
        print("\n\tYou died!  And you only managed to kill {} monsters.".format(gobj.HERO['total_kills']))
        print("\tBetter luck next time.\n\n")

    def monster_died(self):
        if gobj.MONSTER['hp'] <= 0:
            gobj.HERO['total_kills'] += 1
            gobj.HERO['level_kills'] += 1
            print("\nCongratulations!  You killed the {}!".format(gobj.MONSTER['name']))
            print("\tYou have killed {} monsters.".format(gobj.HERO['total_kills']))
            print("\tPrepare for your next fight!\n")
            gobj.MONSTER = get_a_monster_for_level(gobj.HERO['level'])
            return True
        return False

    def level_up(self):
        if (not gobj.HERO['level_kills'] % gobj.HERO['level']):
            gobj.HERO['level'] += 1
            gobj.HERO['hp_max'] += gobj.HERO['level']
            gobj.HERO['level_kills'] = 0
            gobj.HERO['damage_min'] += 1 if gobj.HERO['damage_min'] == 0 else int(math.ceil(gobj.HERO['damage_min'] * 0.1))
            gobj.HERO['damage_max'] += 1 if gobj.HERO['damage_max'] == 0 else int(math.ceil(gobj.HERO['damage_max'] * 0.1))
            gobj.HERO['heal_min'] += 1 if gobj.HERO['heal_min'] == 0 else int(math.ceil(gobj.HERO['heal_min'] * 0.1))
            gobj.HERO['heal_max'] += 1 if gobj.HERO['heal_max'] == 0 else int(math.ceil(gobj.HERO['heal_max'] * 0.1))
            print("\nYou gained a level!\n")
            print("\t You are now level: {}".format(gobj.HERO['level']))
            print("\t You now have {} max hp.".format(gobj.HERO['hp_max']))
            print("\t You deal {} - {} points of damage.".format(gobj.HERO['damage_min'], gobj.HERO['damage_max']))
            print("\t You heal {} - {} when resting.".format(gobj.HERO['heal_min'], gobj.HERO['heal_max']))

    def health_color(self, hp, max_hp):
        colors = [bcolors.FG_BOLD_RED, bcolors.FG_BOLD_YELLOW, bcolors.FG_BOLD_GREEN]
        ratio = hp / max_hp
        return colors[bisect([0.33, 0.66], ratio)]

    @property
    def prompt(self):
        fmt = dict(
            hp_color = self.health_color(gobj.HERO['hp'], gobj.HERO['hp_max']),
            monster_color = self.health_color(gobj.MONSTER['hp'], gobj.MONSTER['hp_max']),
            hero_color = bcolors.BOLD,
            end_color = bcolors.ENDC,
            prompt_color = bcolors.FG_CYAN,
            hero_level = gobj.HERO['level'],
            hero_hp = gobj.HERO['hp'],
            hero_max_hp = gobj.HERO['hp_max'],
            hero_name = gobj.HERO['name'],
            monster_name = gobj.MONSTER['name'],
            monster_hp = gobj.MONSTER['hp'],
            monster_max_hp = gobj.MONSTER['hp_max'],
        )

        prompt = '\n{hero_color}{hero_name}{end_color} - lvl: {hero_level} {hp_color}[{hero_hp}/{hero_max_hp}]{end_color}'
        prompt += ' .. vs .. {monster_color}{monster_name} [{monster_hp}/{monster_max_hp}]{end_color}'
        prompt += ' {prompt_color}#action > {end_color}'
        prompt = prompt.format(**fmt)

        return prompt

    def initialize_game(self):
        gobj.MONSTER_DATA = get_monster_data_from_file('monsters.json')
        gobj.MONSTERS_BY_LEVEL = monsters_by_level(gobj.MONSTER_DATA)
        gobj.HERO = initialize_hero()
        gobj.MONSTER = get_a_monster_for_level(gobj.HERO['level'])


if __name__ == "__main__":
    GameLoop().cmdloop()

