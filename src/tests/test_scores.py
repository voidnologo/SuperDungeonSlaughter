import unittest

from score import format_high_scores


class ScoreTest(unittest.TestCase):

    def test_scores_properly_sorts_and_formats(self):
        raw_scores = [
            {'name': 'frank', 'level': 3, 'kills': 2},
            {'name': 'bob', 'level': 4, 'kills': 9},
            {'name': 'jimmy', 'level': 4, 'kills': 7},
        ]
        formatted = format_high_scores(raw_scores)
        expected = '    NAME    LEVEL  KILLS\n'
        expected += ' 1     bob    4      9  \n'
        expected += ' 2   jimmy    4      7  \n'
        expected += ' 3   frank    3      2  \n'
        self.assertEqual(formatted, expected)
