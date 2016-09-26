import gobj
from bestiary import get_monster_data_from_file, monsters_by_level, get_a_monster_for_level
from commands import Commands
from hero import initialize_hero


class Game(object):

    def __init__(self):
        gobj.MONSTER_DATA = get_monster_data_from_file('monsters.json')
        gobj.MONSTERS_BY_LEVEL = monsters_by_level(gobj.MONSTER_DATA)
        gobj.HERO = initialize_hero()


if __name__ == "__main__":
    gobj.GAME = Game()
    print(gobj.HERO)
    c = Commands()
    c.cmdloop()

