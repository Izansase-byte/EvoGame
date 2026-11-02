import json
import tempfile
import unittest
from pathlib import Path

from simulation import Simulation
from storage import save_simulation, load_simulation


class EventTests(unittest.TestCase):
    def test_save_load_preserves_events(self):
        simulation = Simulation()
        simulation.add_event('Test event')
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'test.json'
            save_simulation(simulation, path)
            restored = load_simulation(path)
        self.assertEqual(restored.events, simulation.events)
        self.assertEqual(restored.events[-1]['message'], 'Test event')

    def test_event_limit(self):
        simulation = Simulation()
        for number in range(60):
            simulation.add_event(f'Event {number}')
        self.assertEqual(len(simulation.events), 50)
        self.assertEqual(simulation.events[0]['message'], 'Event 10')
        self.assertEqual(simulation.events[-1]['message'], 'Event 59')

    def test_load_old_save_without_events(self):
        simulation = Simulation()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'old_save.json'
            save_simulation(simulation, path)
            data = json.loads(path.read_text(encoding='utf-8'))
            data.pop('events')
            path.write_text(json.dumps(data), encoding='utf-8')
            restored = load_simulation(path)
        self.assertEqual(restored.events, [])


if __name__ == '__main__':
    unittest.main()
