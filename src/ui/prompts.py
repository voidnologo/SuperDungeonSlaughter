from bisect import bisect

from src.models.combatant import Combatant
from src.models.hero import Hero
from src.ui.colors import Color


class PromptFormatter:
    """Formats dynamic game prompts with health-colored indicators."""

    HEALTH_THRESHOLDS = [0.33, 0.66]  # Low, medium, high health breakpoints

    @classmethod
    def format_game_prompt(cls, hero: Hero, monster: Combatant) -> str:
        """Create colored prompt showing hero vs monster stats."""
        hero_health_color = cls._get_health_color(hero.hp, hero.hp_max)
        monster_health_color = cls._get_health_color(monster.hp, monster.hp_max)

        parts = [
            f'\n{Color.BOLD}{hero.name}{Color.RESET}',
            f' - lvl: {hero.level}',
            f' {hero_health_color}[{hero.hp}/{hero.hp_max}]{Color.RESET}',
            ' .. vs .. ',
            f'{monster_health_color}{monster.name} [{monster.hp}/{monster.hp_max}]{Color.RESET}',
            f' {Color.FG_CYAN}#action > {Color.RESET}',
        ]

        return ''.join(parts)

    @classmethod
    def _get_health_color(cls, hp: int, max_hp: int) -> Color:
        """Return color based on health percentage (red/yellow/green)."""
        ratio = hp / max_hp if max_hp > 0 else 0
        colors = [Color.FG_BOLD_RED, Color.FG_BOLD_YELLOW, Color.FG_BOLD_GREEN]
        return colors[bisect(cls.HEALTH_THRESHOLDS, ratio)]


def prompt_user(message: str) -> str:
    """Display a prompt and return user input."""
    return input(f'\n{message} >> ')


def prompt_yes_no(message: str) -> bool:
    """Prompt user for yes/no response."""
    choice = None
    while choice not in ['y', 'n']:
        choice = input(f'\n{message} (y/n) >>> ').lower()
    return choice == 'y'
