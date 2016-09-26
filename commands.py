import cmd
import random

import gobj


class Commands(cmd.Cmd):
    prompt = '=> '

    def __init__(self):
        cmd.Cmd.__init__(self)

    def postcmd(self, stop, line):
        self.prompt = '{} +> '.format(random.randint(1, 5))

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
