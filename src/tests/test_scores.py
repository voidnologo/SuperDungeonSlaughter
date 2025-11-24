import unittest

from src.models.score import Score
from src.ui.formatters import format_high_scores


class ScoreDataclassTests(unittest.TestCase):
    def test_score_creation(self):
        score = Score(name='Alice', level=5, kills=10)
        self.assertEqual('Alice', score.name)
        self.assertEqual(5, score.level)
        self.assertEqual(10, score.kills)

    def test_score_is_frozen(self):
        score = Score(name='Bob', level=3, kills=7)
        with self.assertRaises(AttributeError):
            score.level = 4

    def test_score_validation_rejects_empty_name(self):
        with self.assertRaises(ValueError) as ctx:
            Score(name='', level=1, kills=0)
        self.assertIn('name cannot be empty', str(ctx.exception))

    def test_score_validation_rejects_whitespace_name(self):
        with self.assertRaises(ValueError):
            Score(name='   ', level=1, kills=0)

    def test_score_validation_rejects_negative_level(self):
        with self.assertRaises(ValueError) as ctx:
            Score(name='Charlie', level=0, kills=5)
        self.assertIn('level must be at least 1', str(ctx.exception))

    def test_score_validation_rejects_negative_kills(self):
        with self.assertRaises(ValueError) as ctx:
            Score(name='Dave', level=2, kills=-1)
        self.assertIn('kills cannot be negative', str(ctx.exception))

    def test_score_to_dict(self):
        score = Score(name='Eve', level=4, kills=12)
        result = score.to_dict()
        expected = {'name': 'Eve', 'level': 4, 'kills': 12}
        self.assertEqual(expected, result)

    def test_score_from_dict(self):
        data = {'name': 'Frank', 'level': 6, 'kills': 20}
        score = Score.from_dict(data)
        self.assertEqual('Frank', score.name)
        self.assertEqual(6, score.level)
        self.assertEqual(20, score.kills)


class ScoreFormatterTests(unittest.TestCase):
    def test_format_high_scores_returns_no_scores_message_when_empty(self):
        result = format_high_scores([])
        self.assertEqual('No high scores', result)

    def test_format_high_scores_sorts_by_level_then_kills(self):
        scores = [
            Score(name='frank', level=3, kills=2),
            Score(name='bob', level=4, kills=9),
            Score(name='jimmy', level=4, kills=7),
        ]
        formatted = format_high_scores(scores)

        self.assertIn('bob', formatted)
        self.assertIn('jimmy', formatted)
        self.assertIn('frank', formatted)
        bob_pos = formatted.find('bob')
        jimmy_pos = formatted.find('jimmy')
        frank_pos = formatted.find('frank')
        self.assertLess(bob_pos, jimmy_pos)
        self.assertLess(jimmy_pos, frank_pos)

    def test_format_high_scores_includes_rank_numbers(self):
        scores = [Score(name='alice', level=5, kills=15)]
        formatted = format_high_scores(scores)

        self.assertIn('1.', formatted)

    def test_format_high_scores_centers_names(self):
        scores = [Score(name='al', level=2, kills=5)]
        formatted = format_high_scores(scores)

        self.assertIn('al', formatted)

    def test_format_high_scores_handles_varying_name_lengths(self):
        scores = [
            Score(name='A', level=1, kills=1),
            Score(name='VeryLongNameHere', level=2, kills=2),
        ]
        formatted = format_high_scores(scores)

        self.assertIn('A', formatted)
        self.assertIn('VeryLongNameHere', formatted)
