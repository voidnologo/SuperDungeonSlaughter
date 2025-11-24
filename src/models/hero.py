import math
import random
from dataclasses import dataclass, field

from src.models.combatant import CombatStats


@dataclass
class Hero:
    """Player character with combat stats and progression system."""

    name: str
    level: int = 1
    hp: int = 10
    hp_max: int = 10
    total_kills: int = 0
    level_kills: int = 0
    damage_stats: CombatStats = field(default_factory=lambda: CombatStats(0, 3))
    heal_stats: CombatStats = field(default_factory=lambda: CombatStats(1, 4))

    def attack(self, opponent: 'Combatant') -> None:
        """Deal random damage within hero's damage range."""
        damage = random.randint(self.damage_stats.min_value, self.damage_stats.max_value)
        opponent.take_damage(damage)
        print(f'{self.name} deals {damage} damage to the {opponent.name}!')

    def take_damage(self, damage: int) -> None:
        """Reduce HP by damage amount, minimum 0."""
        self.hp = max(0, self.hp - damage)

    def rest(self) -> None:
        """Heal random amount within hero's healing range, capped at max HP."""
        heal = random.randint(self.heal_stats.min_value, self.heal_stats.max_value)
        self.hp = min(self.hp_max, self.hp + heal)
        print(f'{self.name} heals {heal} damage!')

    def level_up(self) -> None:
        """Increase level and stats when kill threshold reached for current level."""
        if not self._should_level_up():
            return

        self.level += 1
        self.hp_max += self.level
        self.level_kills = 0

        self.damage_stats = CombatStats(
            min_value=self._scale_stat(self.damage_stats.min_value, 0.1),
            max_value=self._scale_stat(self.damage_stats.max_value, 0.1),
        )
        self.heal_stats = CombatStats(
            min_value=self._scale_stat(self.heal_stats.min_value, 0.15),
            max_value=self._scale_stat(self.heal_stats.max_value, 0.15),
        )

        self._print_level_up_message()

    def _should_level_up(self) -> bool:
        """Level up when kills equal current level (avoid modulo-zero at level 1)."""
        return self.level_kills > 0 and self.level_kills % self.level == 0

    def _scale_stat(self, current: int, multiplier: float) -> int:
        """Apply percentage increase to stat, minimum +1."""
        if current == 0:
            return 1
        return int(math.ceil(current * (1 + multiplier)))

    def _print_level_up_message(self) -> None:
        """Display level-up notification with new stats."""
        print('\nYou gained a level!\n')
        print(f'\t You are now level: {self.level}')
        print(f'\t You now have {self.hp_max} max hp.')
        print(f'\t You deal {self.damage_stats.min_value} - {self.damage_stats.max_value} points of damage.')
        print(f'\t You heal {self.heal_stats.min_value} - {self.heal_stats.max_value} when resting.')

    def __str__(self) -> str:
        return (
            f'{self.name} - lvl {self.level}: HP> {self.hp} MaxHP> {self.hp_max} '
            f'MinDmg> {self.damage_stats.min_value} MaxDmg> {self.damage_stats.max_value} '
            f'MinHeal> {self.heal_stats.min_value} MaxHeal> {self.heal_stats.max_value} '
            f'TotalKills> {self.total_kills}'
        )
