from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class CombatStats:
    """Combat statistics defining damage or healing ranges."""

    min_value: int
    max_value: int

    def __post_init__(self) -> None:
        if self.min_value < 0:
            raise ValueError('min_value cannot be negative')
        if self.max_value < self.min_value:
            raise ValueError('max_value must be >= min_value')


class Combatant(Protocol):
    """Protocol defining the interface for entities that can engage in combat."""

    name: str
    hp: int
    hp_max: int

    def attack(self, opponent: 'Combatant') -> None:
        """Execute an attack against an opponent."""
        ...

    def take_damage(self, damage: int) -> None:
        """Receive damage from an attack."""
        ...


@dataclass
class CombatResult:
    """Result of a combat action."""

    attacker_name: str
    defender_name: str
    damage: int
    defender_hp_remaining: int
