import math
import random
import csv
from copy import copy

import settings
from creature import Creature

class Simulation:
    def __init__(self, seed=settings.RANDOM_SEED):
        self.seed = seed
        self.events = []
        self.rng = random.Random(seed)
        self.mutation_rate=0.10
        self.energy_multiplier = 1.0
        self.seasons_enabled = True

        self.season_duration = settings.SEASON_DURATION
        self.next_season_duration = settings.SEASON_DURATION
        
        self.creatures = [
            Creature(self.rng)
            for _ in range(settings.INITIAL_POPULATION)
        ]
        
        self.food = []
        self.food_timer = 0
        self.season_index = 0
        self.season_timer = 0
        self.season_name, self.food_interval = settings.SEASONS[0]
        self.elapsed_time = 0
        self.stats_timer = 0
        self.history = []
        self.record_stats()
        
        for _ in range(settings.INITIAL_FOOD_COUNT):
            self.add_food()

        
    def add_food(self):
        self.food.append({
            'x': self.rng.randint(
                settings.FOOD_RADIUS, 
                settings.WIDTH - settings.FOOD_RADIUS),
            'y': self.rng.randint(
                settings.FOOD_RADIUS,
                settings.HEIGHT - settings.FOOD_RADIUS)
        })
    
    def add_event(self,message):
        self.events.append({
            'time': self.elapsed_time,
            'message': message,
        })
        
        self.events = self.events[-50:]
    
    def update(self, dt):
        
        previous_population = len(self.creatures)
        
        if self.seasons_enabled:
            self.season_timer += dt

            while self.season_timer >= self.season_duration:
                self.season_timer -= self.season_duration
                self.season_index = (
                    self.season_index + 1
                ) % len(settings.SEASONS)
                
                self.season_name, self.food_interval = (
                    settings.SEASONS[self.season_index]
                )
                
                self.season_duration = self.next_season_duration
        
                self.add_event(
                    f'Season changed: {settings.season_label(self.season_name)}'
                )        
        
        self.food_timer += dt
        while self.food_timer >= self.food_interval:
            self.add_food()
            self.food_timer -= self.food_interval
        
        for creature in self.creatures:
            target = None
            closest_distance = creature.vision
            
            for food in self.food:
                distance = math.hypot(
                    food['x'] - creature.x,
                    food['y'] - creature.y
                )
                
                if distance < closest_distance:
                    closest_distance = distance
                    target = food
            
            if target is not None and closest_distance > 0:
                dx = target['x'] - creature.x
                dy = target['y'] - creature.y
                
                creature.speed_x = (dx / closest_distance) * creature.speed
                creature.speed_y = (dy / closest_distance) * creature.speed
            
            creature.move(dt,self.energy_multiplier)
            
        for creature in self.creatures:
            for food in self.food[:]:
                distance = math.hypot(
                    food['x'] - creature.x,
                    food['y'] - creature.y
                )
                
                if distance <= (
                    settings.CREATURE_RADIUS + settings.FOOD_RADIUS
                ):
                    self.food.remove(food)
                    creature.energy += settings.FOOD_ENERGY_VALUE
            
        babies = []
        
        for creature in self.creatures:
            if creature.energy >= settings.REPRODUCTION_ENERGY_THRESHOLD:
                creature.energy /= 2
                
                baby = copy(creature)
                
                baby.generation = creature.generation + 1
                
                angle = self.rng.uniform(0, math.tau)
                separation = settings.CREATURE_RADIUS * 2 + 1
                
                baby.x += math.cos(angle) * separation
                baby.y += math.sin(angle) * separation
                
                baby.x = max(
                    settings.CREATURE_RADIUS,
                    min(settings.WIDTH - settings.CREATURE_RADIUS, baby.x)
                )
                
                baby.y = max(
                    settings.CREATURE_RADIUS,
                    min(settings.HEIGHT - settings.CREATURE_RADIUS, baby.y)
                )
                
                baby.speed_x = math.cos(angle) * baby.speed
                baby.speed_y = math.sin(angle) * baby.speed
                
                baby.speed *= self.rng.uniform(0.9, 1.1)
                baby.vision *= self.rng.uniform(0.9, 1.1)
                
                baby.speed *= self.rng.uniform(
                    1-self.mutation_rate,
                    1+self.mutation_rate
                )
                baby.vision *= self.rng.uniform(
                    1 - self.mutation_rate,
                    1 + self.mutation_rate
                )
                
                baby.speed = max(20, min(120, baby.speed))
                baby.vision = max(20, min(180, baby.vision))
                baby.speed_x = math.cos(angle) * baby.speed
                baby.speed_y = math.sin(angle) * baby.speed
                babies.append(baby)
        self.creatures.extend(babies)
        
        if babies:
            self.add_event(f'Born: {len(babies)}')
            
        population_before_deaths = len(self.creatures)
        
        self.creatures = [
            creature
            for creature in self.creatures
            if creature.energy > 0
        ]
        
        deaths = population_before_deaths - len(self.creatures)
        
        if deaths:
            self.add_event(f'Died: {deaths}')
        
        self.elapsed_time += dt
        if previous_population > 0 and not self.creatures:
            self.add_event('Population extinct')
        self.stats_timer += dt

        if self.stats_timer >= 1:
            self.record_stats()
            self.stats_timer %= 1
        
    def record_stats(self):
        population = len(self.creatures)
        average_speed = None
        average_vision = None
        if population:
            average_speed = sum(c.speed for c in self.creatures) / population
            average_vision = sum(c.vision for c in self.creatures) / population

        self.history.append({
            'time': self.elapsed_time,
            'population': population,
            'average_speed': average_speed,
            'average_vision': average_vision,
            'season': self.season_name,
            'seed': self.seed,
            'mutation_rate': self.mutation_rate,
            'energy_multiplier': self.energy_multiplier,
            'food_per_second': 1 / self.food_interval,
            'seasons_enabled': self.seasons_enabled,
            'season_duration': self.season_duration,
            'next_season_duration': self.next_season_duration
        })

    def export_history(self, path):
        fields = [
            'time', 'population', 'average_speed', 'average_vision',
            'season', 'seed', 'mutation_rate', 'energy_multiplier',
            'food_per_second', 'seasons_enabled', 'season_duration',
            'next_season_duration'
        ]
        # Include the current state, even when exporting while paused.
        rows = list(self.history)
        self.record_stats()
        current = self.history.pop()
        if rows and rows[-1]['time'] == current['time']:
            rows[-1] = current
        else:
            rows.append(current)
        with open(path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
