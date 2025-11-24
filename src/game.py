from src.io.repositories import MonsterRepository
from src.io.score_repo import JSONScoreRepository
from src.models.hero import Hero
from src.models.monster import Monster
from src.models.score import Score
from src.ui.prompts import prompt_user


class Game:
    """Main game state container with dependency injection."""

    def __init__(
        self,
        monster_repo: MonsterRepository,
        score_repo: JSONScoreRepository,
    ) -> None:
        self.monster_repo = monster_repo
        self.score_repo = score_repo
        self.hero: Hero = self._create_hero()
        self.monster: Monster = self._spawn_monster()

    def _create_hero(self) -> Hero:
        """Prompt for hero name and create new Hero instance."""
        name = prompt_user("What is your hero's name?")
        return Hero(name=name)

    def _spawn_monster(self) -> Monster:
        """Spawn a monster appropriate for hero's current level."""
        return self.monster_repo.get_monster_for_level(self.hero.level)

    def respawn_monster(self) -> None:
        """Spawn a new monster for the current hero level."""
        self.monster = self._spawn_monster()

    def save_score(self) -> None:
        """Persist current hero's score to repository."""
        score = Score(
            name=self.hero.name,
            level=self.hero.level,
            kills=self.hero.total_kills,
        )
        self.score_repo.add_score(score)
