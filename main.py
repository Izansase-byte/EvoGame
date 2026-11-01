import pygame

import settings
from simulation import Simulation

pygame.init()

screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))

clock = pygame.time.Clock()

simulation = Simulation()
running = True 
paused = False
show_panel = True

font = pygame.font.Font(None, 26)

selected_creature = None

while running:
    dt = clock.tick(settings.FPS) / 1000.0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

            elif event.key == pygame.K_r:
                simulation = Simulation()
                selected_creature = None
                
            elif event.key == pygame.K_h:
                show_panel = not show_panel
                
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x,y = event.pos
                simulation.food.append({
                    'x': x,
                    'y': y
                })
            elif event.button == 3:
                x,y = event.pos
                selected_creature = None

                for creature in simulation.creatures:
                    distance_squared = (
                    (creature.x - x) ** 2 
                    + (creature.y - y) ** 2
                    )
                    if distance_squared <= settings.CREATURE_RADIUS ** 2:
                        selected_creature = creature
                        break
    
    
    if not running:
        break

    if not paused:
        simulation.update(dt)
        
        
        
    screen.fill(settings.BACKGROUND_COLOR)
    
    if selected_creature is not None:
        if selected_creature not in simulation.creatures:
            selected_creature = None
        else:
            pygame.draw.circle(
                screen,
                (100, 130, 180),
                (
                    round(selected_creature.x),
                    round(selected_creature.y)
                ),
                round(selected_creature.vision),
                1
            )
    
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
        
        proportion = (creature.speed - 20) / (120 - 20)
        proportion = max(0, min(1, proportion))
        
        color = (
            round(60 + 195 * proportion),
            round(200 - 120 * proportion),
            120
        )
        
        pygame.draw.circle(
            screen,
            color,
            position,
            settings.CREATURE_RADIUS
        )
        
    pygame.display.set_caption(
        f"Evogame | Things: {len(simulation.creatures)}"
    )
    
    population = len(simulation.creatures)
    
    if population > 0:
        average_speed = sum(
            creature.speed for creature in simulation.creatures
        ) / population
        
        average_vision = sum(
            creature.vision for creature in simulation.creatures
        ) / population
        
    else: 
        average_speed = 0
        average_vision = 0
        
    lines = [
        f'Things: {population}',
        f'Average speed: {average_speed:1f}',
        f'Average vision: {average_vision:1f}',
        f'Food: {len(simulation.food)}',
        'PAUSE | Click SPACE to continue' if paused else 'SPACE: PAUSE | R to restart'
    ]
    
    if selected_creature is not None:
        lines.extend([
            f'Energy: {selected_creature.energy:1f} ',
            f'Speed: {selected_creature.speed:1f} ',
            f'Vision: {selected_creature.vision:1f} ',   
        ])
    if show_panel:
        panel_height = 20 + len(lines) * 28
    
        panel = pygame.Surface((420, panel_height), pygame.SRCALPHA)
        panel.fill((20,25,30,130))
        screen.blit(panel, (0,0))
    
        for index, line in enumerate(lines):
            text = font.render(line, True, (240, 240, 240))
            screen.blit(text, (10, 10 + index * 28))
    
    pygame.display.flip()
    
pygame.quit()