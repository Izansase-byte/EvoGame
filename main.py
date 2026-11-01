import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((1000,700))
pygame.display.set_caption('EvoGame')

clock = pygame.time.Clock()
execution = True

things = []

food = []

for _ in range(50):
    foodie = ({
        'x' : random.randint(5,995),
        'y' : random.randint(5,695)
    })
    food.append(foodie)


for _ in range(20):
    things.append({
        'x': random.uniform(8,992),
        'y': random.uniform(8,692),
        'speed_x': random.uniform(-100,100),
        'speed_y': random.uniform(-70,70),
        'energy': 80,
        'vision': 100,
        'speed': 90
    })

food_timer = 0

while execution:
    dt = clock.tick(60) / 1000
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
    target = None
    closest_distance = thing['vision']

    for foodie in food:
        distance = math.hypot(
            foodie['x'] - thing['x'],
            foodie['y'] - thing['y'],
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
        if thing['x'] >= 1000 - 8:
            thing['x'] = 1000 - 8
            thing['speed_x'] = -abs(thing['speed_x'])
            thing['x'] += thing['speed_x'] * dt
        thing['energy'] -= 5 * dt

    for thing in things:
        if thing['x'] <= 8:
            thing['x'] = 8
            thing['speed_x'] = abs(thing['speed_x'])

    for thing in things:
        if thing['y'] >= 700 - 8:
            thing['y'] = 700 - 8
            thing['speed_y'] = -abs(thing['speed_y'])
            thing['y'] += thing['speed_y'] * dt

    for thing in things:
        if thing['y'] <= 8:
            thing['y'] = 8
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
    things = [thing for thing in things if thing['energy'] > 0]
    screen.fill((20,25,30))

    for foodie in food:
        position = (round(foodie['x']),round(foodie['y']))
        pygame.draw.circle(screen, (240,190,70), position, 3)

    for thing in things:
        pygame.draw.circle(screen, (80,200,120), (round(thing['x']),round(thing['y'])), 8)

    #Prints the drawing
    pygame.display.flip()

    #Limits the game framerate to 60fps


pygame.quit()