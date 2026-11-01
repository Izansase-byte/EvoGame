import pygame

import settings
from simulation import Simulation

pygame.init()

screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))

clock = pygame.time.Clock()

simulation = Simulation()
running = True  

while running:
    dt = clock.tick(settings.FPS) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    if not running:
        break

    simulation.update(dt)
    
    screen.fill(settings.BACKGROUND_COLOR)
    
    for food in simulation.food:
        position = (round(food['x']), round(food['y']))
        
        pygame.draw.circle(
            screen,
            settings.FOOD_COLOR,
            position,
            settings.FOOD_RADIUS
        )
        
    for creature in simulation.creatures:
        position = (round(creature.x), round(creature.y))
        
        pygame.draw.circle(
            screen,
            settings.CREATURE_COLOR,
            position,
            settings.CREATURE_RADIUS
        )
        
    pygame.display.set_caption(
        f"Evogame | Things: {len(simulation.creatures)}"
    )
    
    pygame.display.flip()
    
pygame.quit()