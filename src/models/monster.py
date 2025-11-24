import random
from dataclasses import dataclass


@dataclass(frozen=True)
class MonsterData:
    """Immutable monster template from JSON configuration."""

    name: str
    min_level: int
    max_level: int
    avg_hp: float
    hp_sigma: float
    damage_base: float
    damage_sigma: float

    def __post_init__(self) -> None:
        if self.min_level < 0:
            raise ValueError(f'{self.name}: min_level cannot be negative')
        if self.max_level <= self.min_level:
            raise ValueError(f'{self.name}: max_level must be > min_level')
        if self.avg_hp <= 0:
            raise ValueError(f'{self.name}: avg_hp must be positive')
        if self.damage_base < 0:
            raise ValueError(f'{self.name}: damage_base cannot be negative')


@dataclass
class Monster:
    """Monster instance spawned for combat."""

    name: str
    hp: int
    hp_max: int
    damage_base: float
    damage_sigma: float

    @classmethod
    def from_template(cls, template: MonsterData) -> 'Monster':
        """Create a monster instance with randomized stats based on template."""
        hp = int(random.gauss(template.avg_hp, template.hp_sigma))
        hp = max(1, hp)  # Ensure minimum 1 HP

        return cls(
            name=template.name,
            hp=hp,
            hp_max=hp,
            damage_base=template.damage_base,
            damage_sigma=template.damage_sigma,
        )

    def attack(self, opponent: 'Combatant') -> None:
        """Deal damage with gaussian distribution, clamped to non-negative."""
        damage = int(random.gauss(self.damage_base, self.damage_sigma))
        damage = max(0, damage)  # Critical fix: prevent negative damage
        opponent.take_damage(damage)
        print(f'{self.name} deals {damage} damage to {opponent.name}!')

    def take_damage(self, damage: int) -> None:
        """Reduce HP by damage amount, minimum 0."""
        self.hp = max(0, self.hp - damage)

    def __str__(self) -> str:
        return f'{self.name} HP> {self.hp}/{self.hp_max} BaseDmg> {self.damage_base} DmgSigma> {self.damage_sigma}'
