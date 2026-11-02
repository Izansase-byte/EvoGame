import json
import math
import random
from pathlib import Path

import settings
from creature import Creature
from simulation import Simulation


STATE_FIELDS = (
    'seed', 'mutation_rate', 'energy_multiplier', 'seasons_enabled',
    'season_duration', 'next_season_duration', 'food_timer',
    'season_index', 'season_timer', 'season_name', 'food_interval',
    'elapsed_time', 'stats_timer'
)


def save_simulation(simulation, path):
    path = Path(path)
    data = {
        'format': 1,
        'state': {name: getattr(simulation, name) for name in STATE_FIELDS},
        'creatures': [vars(creature).copy() for creature in simulation.creatures],
        'food': simulation.food,
        'history': simulation.history,
        'events' : simulation.events,
        'random_state': simulation.rng.getstate()
    }
    # Serialize before touching the previous save, then replace atomically.
    text = json.dumps(data, ensure_ascii=False, allow_nan=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(text, encoding='utf-8')
    temporary.replace(path)


def _number(value, name, low=0, high=float('inf')):
    if type(value) not in (int, float) or not math.isfinite(value):
        raise ValueError(f'Invalid numeric value: {name}')
    if not low <= value <= high:
        raise ValueError(f'Value out of range: {name}')


def _tuples(value):
    if isinstance(value, list):
        return tuple(_tuples(item) for item in value)
    return value


def load_simulation(path):
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    try:
        if not isinstance(data, dict) or data.get('format') != 1:
            raise ValueError('Unsupported save format')
        state = data['state']
        if not isinstance(state, dict) or set(state) != set(STATE_FIELDS):
            raise ValueError('Incomplete state')
        for name in STATE_FIELDS:
            if name not in ('seasons_enabled', 'season_name'):
                _number(state[name], name)
        if type(state['seed']) is not int:
            raise ValueError('Invalid seed')
        if type(state['seasons_enabled']) is not bool:
            raise ValueError('Invalid season settings')
        index = state['season_index']
        if type(index) is not int or not 0 <= index < len(settings.SEASONS):
            raise ValueError('Invalid season')
        if state['season_name'] != settings.SEASONS[index][0]:
            raise ValueError('Invalid season name')
        _number(state['mutation_rate'], 'mutation', 0, 0.30)
        _number(state['energy_multiplier'], 'energy cost', 0.1, 3)
        _number(state['food_interval'], 'food', 0.1, 5)
        for name in ('season_duration', 'next_season_duration'):
            _number(state[name], name, 10, 120)
        if state['season_timer'] >= state['season_duration']:
            raise ValueError('Invalid season timer')
        _number(state['stats_timer'], 'sample timer', 0, 1)

        simulation = Simulation(seed=state['seed'])
        for name in STATE_FIELDS:
            setattr(simulation, name, state[name])
        simulation.creatures = []
        template = vars(Creature(random.Random(0)))
        if not isinstance(data['creatures'], list):
            raise ValueError('Invalid population')
        for attributes in data['creatures']:
            if not isinstance(attributes, dict) or set(attributes) != set(template):
                raise ValueError('Incomplete creature')
            for name, value in attributes.items():
                _number(value, name, -float('inf'))
            _number(attributes['x'], 'x', settings.CREATURE_RADIUS, settings.WIDTH - settings.CREATURE_RADIUS)
            _number(attributes['y'], 'y', settings.CREATURE_RADIUS, settings.HEIGHT - settings.CREATURE_RADIUS)
            _number(attributes['speed'], 'speed', 20, 120)
            _number(attributes['vision'], 'vision', 20, 180)
            _number(attributes['energy'], 'energy')
            if type(attributes['generation']) is not int or attributes['generation'] < 0:
                raise ValueError('Invalid generation')
            creature = Creature.__new__(Creature)
            creature.__dict__.update(attributes)
            simulation.creatures.append(creature)

        if not isinstance(data['food'], list):
            raise ValueError('Invalid food list')
        for food in data['food']:
            if not isinstance(food, dict) or set(food) != {'x', 'y'}:
                raise ValueError('Invalid food item')
            _number(food['x'], 'food x', 0, settings.WIDTH)
            _number(food['y'], 'food y', 0, settings.HEIGHT)
        simulation.food = data['food']
        history = data['history']
        if not isinstance(history, list) or not history:
            raise ValueError('Empty or invalid history')
        last_time = -1
        required = {'time', 'population', 'average_speed', 'average_vision', 'season'}
        for sample in history:
            if not isinstance(sample, dict) or not required <= sample.keys():
                raise ValueError('Incomplete sample')
            _number(sample['time'], 'time', 0, state['elapsed_time'])
            _number(sample['population'], 'population')
            if type(sample['population']) is not int or sample['time'] < last_time:
                raise ValueError('History is out of order')
            for name in ('average_speed', 'average_vision'):
                if sample[name] is not None:
                    _number(sample[name], name)
            if sample['season'] not in [season[0] for season in settings.SEASONS]:
                raise ValueError('Invalid season in history')
            last_time = sample['time']
        simulation.history = history
        
        events = data.get('events', [])
        
        if not isinstance(events, list) or len(events) > 50:
            raise ValueError('Event register invalid')
      
        previous_time = -1
        
        for event in events:
            if not isinstance(event, dict):
                raise ValueError('Invalid event')
            
            if set(event) != {'time', 'message'}:
                raise ValueError('Incomplete event')
            
            _number(
                event['time'],
                'Event time',
                0,
                state['elapsed_time']
            )
            
            if event['time'] < previous_time:
                raise ValueError('Events not in order')
            
            if not isinstance(event['message'], str):
                raise ValueError('Invalid event message')
            
            previous_time = event['time']
            
        simulation.events = events
      
        simulation.rng.setstate(_tuples(data['random_state']))
        return simulation
    except (KeyError, TypeError, IndexError, OverflowError) as error:
        raise ValueError('Incomplete or invalid simulation file') from error
