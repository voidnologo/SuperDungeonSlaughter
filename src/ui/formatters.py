from collections.abc import Iterable

from src.models.score import Score
from src.ui.colors import Color, colorize


def format_high_scores(scores: Iterable[Score]) -> str:
    """Format high scores as a colored table, sorted by level then kills (descending)."""
    score_list = list(scores)

    if not score_list:
        return 'No high scores'

    sorted_scores = sorted(score_list, key=lambda s: (s.level, s.kills), reverse=True)

    max_name_width = max(len(s.name) for s in sorted_scores)
    name_width = max(max_name_width, 7)

    header = colorize(f'   {"NAME":^{name_width}}  LEVEL  KILLS   ', Color.FG_BOLD_CYAN, Color.UNDERLINE)
    lines = [header]

    for idx, score in enumerate(sorted_scores, 1):
        rank = colorize(f'{idx:>2}.', Color.FG_BOLD_CYAN)
        line = f'{rank} {score.name:^{name_width}}  {score.level:^5}  {score.kills:>4}'
        lines.append(line)

    return '\n'.join(lines)
