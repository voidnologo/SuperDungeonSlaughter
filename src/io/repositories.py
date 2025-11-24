from typing import Protocol

from src.models.monster import Monster, MonsterData


class MonsterRepository(Protocol):
    """Protocol for loading and managing monster data."""

    def get_monster_for_level(self, level: int) -> Monster:
        """Spawn a random monster appropriate for the given level."""
        ...

    def get_all_templates(self) -> dict[str, MonsterData]:
        """Retrieve all monster templates."""
        ...
