import math
import random
from copy import copy

import settings
from creature import Creature

class Simulation:
    def __init__(self):
        self.creatures = [
            Creature()
            for _ in range(settings.INITIAL_POPULATION)
        ]
        
        self.food = []
        self.food_timer = 0
        self.elapsed_time = 0
        self.stats_timer = 0
        self.history = []
        self.record_stats()
        
        for _ in range(settings.INITIAL_FOOD_COUNT):
            self.add_food()

        
    def add_food(self):
        self.food.append({
            'x': random.randint(
                settings.FOOD_RADIUS, 
                settings.WIDTH - settings.FOOD_RADIUS),
            'y': random.randint(
                settings.FOOD_RADIUS,
                settings.HEIGHT - settings.FOOD_RADIUS)
        })
    
    def update(self, dt):
        self.food_timer += dt
        while self.food_timer >= settings.FOOD_SPAWN_RATE:
            self.add_food()
            self.food_timer -= settings.FOOD_SPAWN_RATE
        
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
            
            creature.move(dt)
            
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
                
                baby.speed *= random.uniform(0.9, 1.1)
                baby.vision *= random.uniform(0.9, 1.1)
                
                baby.speed = max(20, min(120, baby.speed))
                baby.vision = max(20, min(180, baby.vision))
                
                babies.append(baby)
        self.creatures.extend(babies)
        
        self.creatures = [
            creature
            for creature in self.creatures
            if creature.energy > 0
        ]
        self.elapsed_time += dt
        self.stats_timer += dt

        if self.stats_timer >= 1:
            self.record_stats()
            self.stats_timer %= 1
        
    def record_stats(self):
        population = len(self.creatures)
        
        if population > 0:
            average_speed = sum(
                creature.speed for creature in self.creatures
                ) / population
            
            average_vision = sum(
                creature.vision for creature in self.creatures
            ) / population

        else:
            average_speed = None
            average_vision = None

        self.history.append({
            'time': self.elapsed_time,
            'population': population,
            'average_speed': average_speed,
            'average_vision': average_vision
        })