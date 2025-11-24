import cmd

from src.config import MONSTERS_FILE, SCORES_FILE
from src.game import Game
from src.io.monster_repo import JSONMonsterRepository
from src.io.score_repo import JSONScoreRepository
from src.systems.combat import CombatEngine
from src.ui.colors import Color, colorize
from src.ui.formatters import format_high_scores
from src.ui.prompts import PromptFormatter, prompt_yes_no


class GameLoop(cmd.Cmd):
    """Interactive command-line game loop for Super Dungeon Slaughter."""

    doc_header = 'Commands'
    undoc_header = 'No help available'
    ruler = '-'

    def __init__(self) -> None:
        super().__init__()
        self.combat_engine = CombatEngine()
        self.prompt_formatter = PromptFormatter()
        self.game: Game | None = None

    def preloop(self) -> None:
        """Initialize game state before entering command loop."""
        self._print_welcome()
        self._initialize_game()

    def _print_welcome(self) -> None:
        """Display welcome banner."""
        banner = colorize(' Welcome to Super Dungeon Slaughter! ', Color.BOLD, Color.UNDERLINE, Color.BG_RED)
        print(f'{banner}\n')

    def _initialize_game(self) -> None:
        """Create game instance with dependencies."""
        monster_repo = JSONMonsterRepository(MONSTERS_FILE)
        score_repo = JSONScoreRepository(SCORES_FILE)
        self.game = Game(monster_repo, score_repo)

    @property
    def prompt(self) -> str:
        """Dynamic prompt showing hero and monster status."""
        if not self.game:
            return '> '
        return self.prompt_formatter.format_game_prompt(self.game.hero, self.game.monster)

    def do_fight(self, args: str) -> None:
        """Attack the monster (it will counter-attack)."""
        self.game.hero.attack(self.game.monster)
        if not self.combat_engine.is_defeated(self.game.monster):
            self.game.monster.attack(self.game.hero)

    def do_f(self, args: str) -> None:
        """Alias for fight command."""
        self.do_fight(args)

    def do_rest(self, args: str) -> None:
        """Heal some HP (monster will still attack)."""
        self.game.hero.rest()
        self.game.monster.attack(self.game.hero)

    def do_r(self, args: str) -> None:
        """Alias for rest command."""
        self.do_rest(args)

    def do_look(self, args: str) -> None:
        """Inspect hero or monster stats."""
        target = args.lower().strip()

        if not target:
            print("Look at what? Try 'look hero' or 'look monster'")
            return

        if 'hero' in target or self.game.hero.name.lower() in target:
            print(self.game.hero)
        elif 'monster' in target or self.game.monster.name.lower() in target:
            print(self.game.monster)
        else:
            print("You can't see that.")

    def do_l(self, args: str) -> None:
        """Alias for look command."""
        self.do_look(args)

    def do_scores(self, args: str) -> None:
        """Display high score leaderboard."""
        top_scores = self.game.score_repo.iter_top_scores(limit=10)
        print(format_high_scores(top_scores))

    def do_escape(self, args: str) -> bool:
        """Save score and exit game."""
        if prompt_yes_no('Are you sure you wish to quit with your score?'):
            self.game.save_score()
            self.do_scores('')
            return True
        return False

    def do_quit(self, args: str) -> bool:
        """Quit without saving score."""
        print('You are about to lose everything!')
        return True

    def postcmd(self, stop: bool, line: str) -> bool:
        """Check win/loss conditions after each command."""
        if self.combat_engine.is_defeated(self.game.hero):
            self._handle_hero_death()
            return True

        if self.combat_engine.is_defeated(self.game.monster):
            self._handle_monster_death()

        return stop

    def _handle_hero_death(self) -> None:
        """Display death message when hero is defeated."""
        print(f'\n\tYou died! You managed to kill {self.game.hero.total_kills} monsters.')
        print('\tBetter luck next time.\n')

    def _handle_monster_death(self) -> None:
        """Handle monster defeat: update kills, level up, spawn new monster."""
        self.game.hero.total_kills += 1
        self.game.hero.level_kills += 1

        print(f'\nCongratulations! You killed the {self.game.monster.name}!')
        print(f'\tYou have killed {self.game.hero.total_kills} monsters.')
        print('\tPrepare for your next fight!\n')

        self.game.hero.level_up()
        self.game.respawn_monster()


def main() -> None:
    """Entry point for the game."""
    GameLoop().cmdloop()


if __name__ == '__main__':
    main()
