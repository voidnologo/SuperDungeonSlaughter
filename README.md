# Super Dungeon Slaughter 🐉⚔️

A text-based dungeon crawler RPG where you battle increasingly powerful monsters to achieve the highest score.

## Quick Start

### Installation

```bash
pip install -e ".[dev]"
```

### Play the Game

```bash
dungeon
```

Or run directly:
```bash
python -m src.main
```

## How to Play

### Commands

- `fight` or `f` - Attack the monster (it will counter-attack)
- `rest` or `r` - Heal some HP (monster will still attack)
- `look <target>` or `l <target>` - Inspect hero or monster stats
- `scores` - Display high score leaderboard
- `escape` - Save your score and exit
- `quit` - Quit without saving
- `help` - Show available commands

### Gameplay

1. Create your hero by entering a name
2. Fight monsters appropriate for your level
3. Defeat monsters to gain experience and level up
4. Each level increases your stats and unlocks tougher monsters
5. Try to survive as long as possible and achieve a high score

## Game Mechanics

### Combat
- Attacking deals damage within your damage range
- Resting heals HP but the monster still attacks
- Combat uses statistical variance for realistic unpredictability

### Leveling
- Defeat monsters to gain kills
- Level up after killing N monsters (where N = your current level)
- Each level increases your maximum HP and combat effectiveness

### Monsters
11 unique monster types from weakest to strongest:
- **Kobold, Slime, Goblin** - Early game threats
- **Werebat, Rabid Wombat** - Mid-level challenges
- **Orc, Undying** - Dangerous foes
- **Drake, Lesser Dragon** - Elite enemies
- **Kitten, Greater Dragon** - Endgame bosses

Monsters scale with your level, ensuring constant challenge.

## Project Structure

```
SuperDungeonSlaughter/
├── src/
│   ├── main.py              # Game entry point
│   ├── game.py              # Game orchestration
│   ├── config.py            # Configuration
│   ├── models/              # Game entities (Hero, Monster, Score)
│   ├── systems/             # Game logic (Combat)
│   ├── io/                  # Data persistence (Repositories)
│   ├── ui/                  # User interface (Colors, Prompts, Formatters)
│   └── tests/               # Test suite (65 tests)
├── data/
│   ├── monsters.json        # Monster definitions
│   └── scores.json          # High scores
├── pyproject.toml           # Project configuration
├── run_tests.py             # Test runner
└── README.md                # This file
```

## Development

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test file
python -m unittest src.tests.test_hero
```

### Code Formatting

```bash
# Format code
ruff format src/

# Sort imports
isort src/

# Lint
ruff check src/
```

## Requirements

- Python 3.13 or higher
- No external dependencies required for gameplay
- Development tools: `ruff`, `isort` (installed with `pip install -e ".[dev]"`)

## High Scores

Your score is based on:
- **Level achieved** (primary factor)
- **Total kills** (tiebreaker)

High scores are saved to `data/scores.json` and persist between games.

## License

MIT License
