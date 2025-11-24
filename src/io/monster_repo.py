import json
import random
from collections import defaultdict
from pathlib import Path

from src.models.monster import Monster, MonsterData


class MonsterNotFoundError(Exception):
    """Raised when no monsters are available for a given level."""

    pass


class JSONMonsterRepository:
    """Repository for loading monster data from JSON files."""

    def __init__(self, data_file: Path) -> None:
        self.data_file = data_file
        self._templates: dict[str, MonsterData] = {}
        self._level_groups: dict[int, list[str]] = defaultdict(list)
        self._load_monsters()

    def _load_monsters(self) -> None:
        """Load and validate monster data from JSON file."""
        with self.data_file.open() as f:
            raw_data = json.load(f)

        for name, data in raw_data.items():
            template = MonsterData(
                name=name,
                min_level=data['min_level'],
                max_level=data['max_level'],
                avg_hp=data['avg_hp'],
                hp_sigma=data['hp_sigma'],
                damage_base=data['damage_base'],
                damage_sigma=data['damage_sigma'],
            )
            self._templates[name] = template
            self._index_by_level(template)

    def _index_by_level(self, template: MonsterData) -> None:
        """Build level-based lookup for fast monster selection."""
        for level in range(template.min_level, template.max_level):
            self._level_groups[level].append(template.name)

    def get_monster_for_level(self, level: int) -> Monster:
        """Spawn a random monster appropriate for the level.

        Falls back to highest available level if exact match not found.
        """
        available = self._level_groups.get(level)

        if not available:
            available = self._find_fallback_monsters(level)

        if not available:
            raise MonsterNotFoundError(f'No monsters defined for level {level} or nearby levels')

        monster_name = random.choice(available)
        template = self._templates[monster_name]
        return Monster.from_template(template)

    def _find_fallback_monsters(self, level: int) -> list[str]:
        """Find monsters from nearest available level as fallback."""
        if not self._level_groups:
            return []

        closest_level = min(self._level_groups.keys(), key=lambda lvl: abs(lvl - level))
        return self._level_groups[closest_level]

    def get_all_templates(self) -> dict[str, MonsterData]:
        """Retrieve all monster templates."""
        return self._templates.copy()
