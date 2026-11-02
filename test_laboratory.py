import csv
import tempfile
import unittest
from pathlib import Path

import settings
from laboratory import Laboratory
from simulation import Simulation


class LaboratoryTests(unittest.TestCase):
    def setUp(self):
        self.simulation = Simulation()
        self.lab = Laboratory()

    def test_presets_keep_population_and_history(self):
        creatures = list(self.simulation.creatures)
        history = list(self.simulation.history)
        for name, rate, mutation in [
            ('abundance', 8.0, 0.10),
            ('scarcity', 0.5, 0.10),
            ('high_mutation', 4.0, 0.30)
        ]:
            self.lab.apply('preset_' + name, self.simulation)
            self.assertAlmostEqual(1 / self.simulation.food_interval, rate)
            self.assertEqual(self.simulation.mutation_rate, mutation)
            self.assertFalse(self.simulation.seasons_enabled)
            self.assertEqual(self.simulation.creatures, creatures)
            self.assertEqual(self.simulation.history, history)

    def test_button_limits(self):
        for action, attribute, low, high in [
            ('mutation', 'mutation_rate', 0, 0.30),
            ('energy', 'energy_multiplier', 0.1, 3.0),
            ('duration', 'next_season_duration', 10, 120)
        ]:
            for _ in range(150):
                self.lab.apply(action + '_minus', self.simulation)
            self.assertEqual(getattr(self.simulation, attribute), low)
            for _ in range(150):
                self.lab.apply(action + '_plus', self.simulation)
            self.assertEqual(getattr(self.simulation, attribute), high)
        for _ in range(100):
            self.lab.apply('food_minus', self.simulation)
        self.assertAlmostEqual(1 / self.simulation.food_interval, 0.2)
        for _ in range(100):
            self.lab.apply('food_plus', self.simulation)
        self.assertAlmostEqual(1 / self.simulation.food_interval, 10)

    def test_reset_preserves_creatures(self):
        creature = self.simulation.creatures[0]
        self.lab.apply_preset('high_mutation', self.simulation)
        self.simulation.season_timer = 15
        self.lab.apply('reset_values', self.simulation)
        self.assertIs(self.simulation.creatures[0], creature)
        self.assertEqual(self.simulation.mutation_rate, 0.10)
        self.assertEqual(self.simulation.energy_multiplier, 1.0)
        self.assertTrue(self.simulation.seasons_enabled)
        self.assertEqual(self.simulation.season_timer, 0)
        self.assertEqual(self.simulation.next_season_duration, settings.SEASON_DURATION)
        self.assertEqual(self.simulation.food_interval, settings.SEASONS[0][1])

    def test_csv_exports_paused_changes_without_altering_history(self):
        history = list(self.simulation.history)
        self.lab.apply_preset('scarcity', self.simulation)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'experiment.csv'
            self.simulation.export_history(path)
            with path.open(encoding='utf-8', newline='') as file:
                rows = list(csv.DictReader(file))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['seasons_enabled'], 'False')
        self.assertEqual(float(rows[0]['food_per_second']), 0.5)
        self.assertEqual(int(rows[0]['seed']), self.simulation.seed)
        self.assertEqual(self.simulation.history, history)

    def test_season_and_extinction_statistics(self):
        self.simulation.creatures.clear()
        for _ in range(1860):
            self.simulation.update(1 / 60)
        self.assertEqual(self.simulation.season_index, 1)
        self.assertIsNone(self.simulation.history[-1]['average_speed'])
        self.assertEqual(self.simulation.history[-1]['population'], 0)
        self.assertEqual(self.simulation.history[-1]['season'], settings.SEASONS[1][0])


    def test_independent_simulations_repeat_the_same_seed(self):
        first = Simulation(seed=123)
        second = Simulation(seed=123)
        other = Simulation(seed=999)
        for _ in range(1200):
            first.update(1 / 60)
            other.update(1 / 60)
            second.update(1 / 60)
        self.assertEqual(first.history, second.history)
        self.assertEqual(first.food, second.food)
        self.assertEqual([vars(c) for c in first.creatures], [vars(c) for c in second.creatures])

    def test_seed_buttons_and_restart(self):
        self.lab.apply('seed_plus', self.simulation)
        self.assertEqual(self.simulation.seed, settings.RANDOM_SEED)
        self.assertEqual(self.lab.seed_value, settings.RANDOM_SEED + 1)
        self.simulation.update(1 / 60)
        self.lab.apply('restart_seed', self.simulation)
        self.assertEqual(self.simulation.seed, settings.RANDOM_SEED + 1)
        self.assertEqual(self.simulation.elapsed_time, 0)
        self.assertEqual(len(self.simulation.history), 1)
        self.assertEqual(len(self.simulation.creatures), settings.INITIAL_POPULATION)
        self.lab.seed_value = 0
        self.lab.apply('seed_minus', self.simulation)
        self.assertEqual(self.lab.seed_value, 0)


    def test_save_load_continues_identically(self):
        from storage import save_simulation, load_simulation
        original = Simulation(seed=77)
        self.lab.apply_preset('high_mutation', original)
        for _ in range(1800):
            original.update(1 / 60)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'state.json'
            save_simulation(original, path)
            restored = load_simulation(path)
        self.assertEqual(original.history, restored.history)
        self.assertEqual(original.rng.getstate(), restored.rng.getstate())
        for _ in range(600):
            original.update(1 / 60)
            restored.update(1 / 60)
        self.assertEqual(original.history, restored.history)
        self.assertEqual(original.food, restored.food)
        self.assertEqual([vars(c) for c in original.creatures], [vars(c) for c in restored.creatures])

    def test_load_rejects_corrupt_and_invalid_saves(self):
        import json
        from storage import save_simulation, load_simulation
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'state.json'
            for text in ('broken json', '{}', '[]'):
                path.write_text(text, encoding='utf-8')
                with self.assertRaises(ValueError):
                    load_simulation(path)
            save_simulation(self.simulation, path)
            data = json.loads(path.read_text(encoding='utf-8'))
            data['state']['food_interval'] = 0
            path.write_text(json.dumps(data), encoding='utf-8')
            with self.assertRaises(ValueError):
                load_simulation(path)

    def test_empty_population_can_be_saved(self):
        from storage import save_simulation, load_simulation
        self.simulation.creatures.clear()
        self.simulation.update(1)
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'state.json'
            save_simulation(self.simulation, path)
            restored = load_simulation(path)
        self.assertEqual(restored.creatures, [])
        self.assertIsNone(restored.history[-1]['average_speed'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
