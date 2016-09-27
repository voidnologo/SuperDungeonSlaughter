import cmd
import random

from bestiary import get_monster_data_from_file, monsters_by_level, get_a_monster_for_level
from colors import bcolors
import gobj
from hero import initialize_hero


class GameLoop(cmd.Cmd):
    welcome = "{}{}{} Welcome to Super Dungeon Slaughter! {}\\nn".format(bcolors.BOLD, bcolors.UNDERLINE, bcolors.BG_RED, bcolors.ENDC)

    def preloop(self):
        print(self.welcome)
        self.initialize_game()

    def do_f(self, args):
        print('f')
        pass

    def do_fight(self, args):
        print('fight')
        pass

    def do_r(self, args):
        print('r')
        pass

    def do_rest(self, args):
        print('rest')
        pass

    def do_escape(self, args):
        print('escape')
        pass

    def do_quit(self, args):
        print('quit')
        pass

    def do_look(self, args):
        print('look')
        pass
        # if args == 'room':


    def health_color(self, hp, max_hp):
        colors = ((0.66, bcolors.FG_BOLD_GREEN), (0.33, bcolors.FG_BOLD_RED), (0.0, bcolors.FG_BOLD_RED))
        ratio = hp / max_hp
        return [c[1] for c in colors if ratio > c[0]][0]

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
        )

        prompt = '{hero_color}{hero_name}{end_color} - lvl: {hero_level} {hp_color}[{hero_hp}/{hero_max_hp}]{end_color}'
        prompt += ' .. vs .. {monster_color}{monster_name}{end_color}'
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

