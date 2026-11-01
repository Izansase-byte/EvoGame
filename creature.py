import random
import settings

class Creature:
    def __init__(self):
        self.x = random.uniform(settings.CREATURE_RADIUS, settings.WIDTH - settings.CREATURE_RADIUS)
        self.y = random.uniform(settings.CREATURE_RADIUS, settings.HEIGHT - settings.CREATURE_RADIUS)
        self.speed_x = random.uniform(-100,100)
        self.speed_y = random.uniform(-70,70)
        self.vision = settings.INITIAL_VISION
        self.energy = settings.INITIAL_ENERGY
        self.speed = settings.INITIAL_SPEED

    def move(self, dt):
        self.x += self.speed_x * dt
        self.y += self.speed_y * dt
        
        radius = settings.CREATURE_RADIUS
        
        if self.x >= settings.WIDTH - radius:
            self.x = settings.WIDTH - radius
            self.speed_x = -abs(self.speed_x)
        elif self.x <= radius:
            self.x = radius
            self.speed_x = abs(self.speed_x)
        
        if self.y >= settings.HEIGHT - radius:
            self.y = settings.HEIGHT - radius
            self.speed_y = -abs(self.speed_y)
        elif self.y <= radius:
            self.y = radius
            self.speed_y = abs(self.speed_y)
            
        self.energy -= settings.ENERGY_LOSS_RATE * dt