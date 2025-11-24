import json
import logging
from collections.abc import Iterator
from pathlib import Path

from src.models.score import Score

logger = logging.getLogger(__name__)


class JSONScoreRepository:
    """Repository for persisting high scores to JSON."""

    def __init__(self, data_file: Path) -> None:
        self.data_file = data_file

    def load_scores(self) -> list[Score]:
        """Load all scores from file, returning empty list on error."""
        if not self.data_file.exists():
            return []

        try:
            with self.data_file.open() as f:
                raw_data = json.load(f)
            return [Score.from_dict(entry) for entry in raw_data]
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f'Failed to load scores from {self.data_file}: {e}')
            return []

    def save_scores(self, scores: list[Score]) -> None:
        """Persist scores to file."""
        try:
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            with self.data_file.open('w') as f:
                json.dump([s.to_dict() for s in scores], f, indent=2)
        except OSError as e:
            logger.error(f'Failed to save scores to {self.data_file}: {e}')

    def add_score(self, score: Score) -> None:
        """Add a new score to the repository."""
        scores = self.load_scores()
        scores.append(score)
        self.save_scores(scores)

    def iter_top_scores(self, limit: int = 10) -> Iterator[Score]:
        """Yield top N scores sorted by level (desc), then kills (desc)."""
        scores = self.load_scores()
        sorted_scores = sorted(scores, key=lambda s: (s.level, s.kills), reverse=True)
        yield from sorted_scores[:limit]
