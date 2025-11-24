from dataclasses import dataclass


@dataclass(frozen=True)
class Score:
    """Immutable high score entry."""

    name: str
    level: int
    kills: int

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError('Score name cannot be empty')
        if self.level < 1:
            raise ValueError('Score level must be at least 1')
        if self.kills < 0:
            raise ValueError('Score kills cannot be negative')

    def to_dict(self) -> dict[str, int | str]:
        """Convert to dictionary for JSON serialization."""
        return {'name': self.name, 'level': self.level, 'kills': self.kills}

    @classmethod
    def from_dict(cls, data: dict[str, int | str]) -> 'Score':
        """Create Score from dictionary."""
        return cls(
            name=str(data['name']),
            level=int(data['level']),
            kills=int(data['kills']),
        )
