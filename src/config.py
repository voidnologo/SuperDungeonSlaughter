from pathlib import Path

# Project structure
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'

# Data files
MONSTERS_FILE = DATA_DIR / 'monsters.json'
SCORES_FILE = DATA_DIR / 'scores.json'
