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
            
        babies = []
        
        for creature in self.creatures:
            if creature.energy >= settings.REPRODUCTION_ENERGY_THRESHOLD:
                creature.energy /= 2
                babies.append(copy(creature))
                
        self.creatures.extend(babies)
        
        self.creatures = [
            creature
            for creature in self.creatures
            if creature.energy > 0
        ]