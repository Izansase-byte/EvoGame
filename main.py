import pygame
import random
import math
import settings

pygame.init()

screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption('EvoGame')

clock = pygame.time.Clock()
execution = True

things = []

food = []

for _ in range(settings.INITIAL_FOOD_COUNT):
    foodie = ({
        'x' : random.randint(5,995),
        'y' : random.randint(5,695)
    })
    food.append(foodie)


for _ in range(settings.INITIAL_POPULATION):
    things.append({
        'x': random.uniform(8,992),
        'y': random.uniform(8,692),
        'speed_x': random.uniform(-100,100),
        'speed_y': random.uniform(-70,70),
        'energy': settings.INITIAL_ENERGY,
        'vision': settings.INITIAL_VISION,
        'speed': settings.INITIAL_SPEED
    })

food_timer = 0

while execution:
    dt = clock.tick(settings.FPS) / 1000
    food_timer += dt
    while food_timer >= 0.5:
        food.append({
            'x' : random.randint(5,995),
            'y' : random.randint(5,695)
        })
        food_timer -= 0.5

    # Reads the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            execution = False
    
    for thing in things:
        target = None
        closest_distance = thing['vision']

        for foodie in food:
            distance = math.hypot(
                foodie['x'] - thing['x'],
                foodie['y'] - thing['y']
            )
            if distance < closest_distance:
                closest_distance = distance
                target = foodie

            if target is not None and closest_distance > 0:
                dx = target['x'] - thing['x']
                dy = target['y'] - thing['y']

                thing['speed_x'] = (dx / closest_distance) * thing['speed']
                thing['speed_y'] = (dy / closest_distance) * thing['speed']

    for thing in things:
        thing['x'] += thing['speed_x'] * dt
        thing['y'] += thing['speed_y'] * dt

    for thing in things:
        if thing['x'] >= settings.WIDTH - settings.CREATURE_RADIUS:
            thing['x'] = settings.WIDTH - settings.CREATURE_RADIUS
            thing['speed_x'] = -abs(thing['speed_x'])
            thing['x'] += thing['speed_x'] * dt
        thing['energy'] -= settings.ENERGY_LOSS_RATE * dt

    for thing in things:
        if thing['x'] <= settings.CREATURE_RADIUS:
            thing['x'] = settings.CREATURE_RADIUS
            thing['speed_x'] = abs(thing['speed_x'])

    for thing in things:
        if thing['y'] >= settings.HEIGHT - settings.CREATURE_RADIUS:
            thing['y'] = settings.HEIGHT - settings.CREATURE_RADIUS
            thing['speed_y'] = -abs(thing['speed_y'])
            thing['y'] += thing['speed_y'] * dt

    for thing in things:
        if thing['y'] <= settings.CREATURE_RADIUS:
            thing['y'] = settings.CREATURE_RADIUS
            thing['speed_y'] = abs(thing['speed_y'])
    for thing in things:
        for foodie in food[:]: 
            distance = math.hypot(
                foodie['x'] - thing['x'],
                foodie['y'] - thing['y'],
            )
            if distance <= 11:
                food.remove(foodie)
                thing['energy'] += 30

    #Fills the background
    
    babies = []
    
    for thing in things:
        if thing['energy'] >= 140:
            thing['energy'] /= 2
            
            baby = thing.copy()
            babies.append(baby)
            
    things.extend(babies)
    
    things = [thing for thing in things if thing['energy'] > 0]
    screen.fill((settings.BACKGROUND_COLOR))

    for foodie in food:
        position = (round(foodie['x']),round(foodie['y']))
        pygame.draw.circle(screen, (settings.FOOD_COLOR), position, settings.FOOD_RADIUS)

    for thing in things:
        pygame.draw.circle(screen, (settings.CREATURE_COLOR), (round(thing['x']),round(thing['y'])), settings.CREATURE_RADIUS)

    pygame.display.set_caption(f'EvoGame | Things: {len(things)} | Food: {len(food)}')

    #Prints the drawing
    pygame.display.flip()

    #Limits the game framerate to 60fps


pygame.quit()