import json
import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile

from src.io.monster_repo import JSONMonsterRepository, MonsterNotFoundError
from src.io.score_repo import JSONScoreRepository
from src.models.monster import Monster, MonsterData
from src.models.score import Score


class JSONMonsterRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_file = NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.test_data = {
            'Goblin': {
                'min_level': 0,
                'max_level': 3,
                'avg_hp': 5,
                'hp_sigma': 0.5,
                'damage_base': 2,
                'damage_sigma': 1,
            },
            'Orc': {
                'min_level': 2,
                'max_level': 6,
                'avg_hp': 8,
                'hp_sigma': 2,
                'damage_base': 4,
                'damage_sigma': 1.5,
            },
        }
        json.dump(self.test_data, self.temp_file)
        self.temp_file.close()
        self.repo = JSONMonsterRepository(Path(self.temp_file.name))

    def tearDown(self):
        Path(self.temp_file.name).unlink()

    def test_loads_monster_templates(self):
        templates = self.repo.get_all_templates()
        self.assertEqual(2, len(templates))
        self.assertIn('Goblin', templates)
        self.assertIn('Orc', templates)

    def test_template_has_correct_data(self):
        templates = self.repo.get_all_templates()
        goblin = templates['Goblin']
        self.assertIsInstance(goblin, MonsterData)
        self.assertEqual('Goblin', goblin.name)
        self.assertEqual(0, goblin.min_level)
        self.assertEqual(3, goblin.max_level)

    def test_get_monster_for_level_returns_appropriate_monster(self):
        monster = self.repo.get_monster_for_level(1)
        self.assertIsInstance(monster, Monster)
        self.assertIn(monster.name, ['Goblin', 'Orc'])

    def test_get_monster_for_level_respects_level_ranges(self):
        monster = self.repo.get_monster_for_level(0)
        self.assertEqual('Goblin', monster.name)

    def test_get_monster_for_level_with_multiple_options_returns_valid_choice(self):
        monster = self.repo.get_monster_for_level(2)
        self.assertIn(monster.name, ['Goblin', 'Orc'])

    def test_get_monster_for_level_falls_back_when_exact_match_not_found(self):
        monster = self.repo.get_monster_for_level(10)
        self.assertIsInstance(monster, Monster)

    def test_get_monster_for_empty_repository_raises_error(self):
        empty_file = NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        json.dump({}, empty_file)
        empty_file.close()

        repo = JSONMonsterRepository(Path(empty_file.name))

        with self.assertRaises(MonsterNotFoundError):
            repo.get_monster_for_level(1)

        Path(empty_file.name).unlink()


class JSONScoreRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temp_file = NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.repo = JSONScoreRepository(Path(self.temp_file.name))

    def tearDown(self):
        Path(self.temp_file.name).unlink()

    def test_load_scores_returns_empty_list_when_file_does_not_exist(self):
        file_path = Path(self.temp_file.name)
        file_path.unlink()
        scores = self.repo.load_scores()
        self.assertEqual([], scores)
        file_path.touch()  # Recreate for tearDown

    def test_save_and_load_scores(self):
        scores = [Score(name='Alice', level=3, kills=10), Score(name='Bob', level=5, kills=15)]

        self.repo.save_scores(scores)
        loaded = self.repo.load_scores()

        self.assertEqual(2, len(loaded))
        self.assertEqual('Alice', loaded[0].name)
        self.assertEqual('Bob', loaded[1].name)

    def test_add_score_appends_to_existing_scores(self):
        existing = [Score(name='Charlie', level=2, kills=5)]
        self.repo.save_scores(existing)

        new_score = Score(name='Dave', level=4, kills=12)
        self.repo.add_score(new_score)

        loaded = self.repo.load_scores()
        self.assertEqual(2, len(loaded))
        self.assertEqual('Dave', loaded[1].name)

    def test_iter_top_scores_returns_sorted_scores(self):
        scores = [
            Score(name='Low', level=1, kills=2),
            Score(name='High', level=5, kills=20),
            Score(name='Mid', level=3, kills=10),
        ]
        self.repo.save_scores(scores)

        top_scores = list(self.repo.iter_top_scores(limit=3))

        self.assertEqual(3, len(top_scores))
        self.assertEqual('High', top_scores[0].name)
        self.assertEqual('Mid', top_scores[1].name)
        self.assertEqual('Low', top_scores[2].name)

    def test_iter_top_scores_limits_results(self):
        scores = [Score(name=f'Player{i}', level=i, kills=i * 2) for i in range(1, 6)]
        self.repo.save_scores(scores)

        top_scores = list(self.repo.iter_top_scores(limit=3))

        self.assertEqual(3, len(top_scores))

    def test_iter_top_scores_sorts_by_level_then_kills(self):
        scores = [
            Score(name='SameLevel1', level=5, kills=10),
            Score(name='SameLevel2', level=5, kills=15),
            Score(name='LowerLevel', level=4, kills=20),
        ]
        self.repo.save_scores(scores)

        top_scores = list(self.repo.iter_top_scores(limit=3))

        self.assertEqual('SameLevel2', top_scores[0].name)
        self.assertEqual('SameLevel1', top_scores[1].name)
        self.assertEqual('LowerLevel', top_scores[2].name)

    def test_load_scores_handles_corrupted_json(self):
        with open(self.temp_file.name, 'w') as f:
            f.write('{ invalid json')

        scores = self.repo.load_scores()
        self.assertEqual([], scores)
