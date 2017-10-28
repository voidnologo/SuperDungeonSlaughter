import simplejson as json
from operator import itemgetter

from colors import bcolors
from utils import data_file_path

SCORE_FILE = 'scores.json'


def _read_score_file():
    try:
        with open(data_file_path(SCORE_FILE), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.scanner.JSONDecodeError:
        return None


def _write_score_file(data):
    try:
        with open(data_file_path(SCORE_FILE), 'w') as f:
            json.dump(data, f)
    except IOError:
        print('Unable to write high scores file.')


def format_high_scores(scores):
    scores = sorted(scores, key=itemgetter('level', 'kills'), reverse=True)
    width = max(max((len(x['name']) for x in scores)), 7)
    display = f'   {bcolors.FG_BOLD_CYAN}{bcolors.UNDERLINE}{"NAME":^{width}}  LEVEL  KILLS   {bcolors.ENDC}\n'
    for idx, s in enumerate(scores[:10], 1):
        display += f'{bcolors.FG_BOLD_CYAN}{idx:>2}.{bcolors.ENDC} {s["name"]:^{width}}  {s["level"]:^5}  {s["kills"]:>4}\n'
    return display


def get_high_scores():
    scores = _read_score_file()
    if scores:
        return format_high_scores(scores)
    return 'No high scores'


def write_score(hero):
    scores = _read_score_file()
    score = {
        'name': hero.name,
        'level': hero.level,
        'kills': hero.total_kills
    }
    if scores:
        scores.append(score)
    else:
        scores = [score]
    _write_score_file(scores)
