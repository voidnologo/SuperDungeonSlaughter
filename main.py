import cmd
from bisect import bisect

from colors import bcolors
from gobj import Game


class GameLoop(cmd.Cmd):
    welcome = "{}{}{} Welcome to Super Dungeon Slaughter! {}\n\n".format(
        bcolors.BOLD, bcolors.UNDERLINE, bcolors.BG_RED, bcolors.ENDC
    )
    doc_header = 'Commands'
    undoc_header = 'No help available'
    ruler = '-'

    def preloop(self):
        print(self.welcome)
        self.initialize_game()

    def do_f(self, args):
        "Fight! Attack the monster! Beware, it will fight back!"
        self.do_fight(args)

    def do_fight(self, args):
        "Fight! Attack the monster! Beware, it will fight back!"
        self.game.hero.attack(self.game.monster)
        self.game.monster.attack(self.game.hero)

    def do_r(self, args):
        "Rest. Regain some hit points. Watch out, the monster will still fight!"
        self.do_rest(args)

    def do_rest(self, args):
        "Rest. Regain some hit points. Watch out, the monster will still fight!"
        self.game.hero.rest()
        self.game.monster.attack(self.game.hero)

    def do_escape(self, args):
        "Leave the game with your current score"
        print('escape')
        pass

    def do_quit(self, args):
        "Quit - lose everything!"
        print('quit')
        return True

    def do_l(self, args):
        "Look {target}"
        self.do_look(args)

    def do_look(self, args):
        "Look {target}"
        args = args.lower()
        if args in 'hero' or args in self.game.hero.name.lower():
            print(self.game.hero)
        elif args in 'monster' or args in self.game.monster.name.lower():
            print(self.game.monster)
        else:
            print("You can't see that.'")

    def postcmd(self, stop, line):
        if self.game.hero.hp <= 0:
            self.lose_game()
            return True
        if self.monster_died():
            self.game.hero.level_up()

    def lose_game(self):
        print("\n\tYou died!  And you only managed to kill {} monsters.".format(self.game.hero.total_kills))
        print("\tBetter luck next time.\n\n")

    def monster_died(self):
        if self.game.monster.hp <= 0:
            self.game.hero.total_kills += 1
            self.game.hero.level_kills += 1
            print("\nCongratulations!  You killed the {}!".format(self.game.monster.name))
            print("\tYou have killed {} monsters.".format(self.game.hero.total_kills))
            print("\tPrepare for your next fight!\n")
            self.game.monster = self.game.bestiary.get_a_monster_for_level(self.game.hero.level)
            return True
        return False

    def health_color(self, hp, max_hp):
        colors = [bcolors.FG_BOLD_RED, bcolors.FG_BOLD_YELLOW, bcolors.FG_BOLD_GREEN]
        ratio = hp / max_hp
        return colors[bisect([0.33, 0.66], ratio)]

    @property
    def prompt(self):
        fmt = dict(
            hp_color=self.health_color(self.game.hero.hp, self.game.hero.hp_max),
            monster_color=self.health_color(self.game.monster.hp, self.game.monster.hp_max),
            hero_color=bcolors.BOLD,
            end_color=bcolors.ENDC,
            prompt_color=bcolors.FG_CYAN,
            hero_level=self.game.hero.level,
            hero_hp=self.game.hero.hp,
            hero_max_hp=self.game.hero.hp_max,
            hero_name=self.game.hero.name,
            monster_name=self.game.monster.name,
            monster_hp=self.game.monster.hp,
            monster_max_hp=self.game.monster.hp_max,
        )
        prompt = '\n{hero_color}{hero_name}{end_color} - lvl: {hero_level} {hp_color}[{hero_hp}/{hero_max_hp}]{end_color}'  # noqa: 401
        prompt += ' .. vs .. {monster_color}{monster_name} [{monster_hp}/{monster_max_hp}]{end_color}'
        prompt += ' {prompt_color}#action > {end_color}'
        return prompt.format(**fmt)

    def initialize_game(self):
        self.game = Game()


if __name__ == "__main__":
    GameLoop().cmdloop()
