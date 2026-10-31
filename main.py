import pygame

pygame.init()

screen = pygame.display.set_mode((1000,700))
pygame.display.set_caption('EvoGame')

clock = pygame.time.Clock()
execution = True

while execution:
    # Reads the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            execution = False
    #Fills the background
    screen.fill((20,25,30))

    #Prints the drawing
    pygame.display.flip()

    #Limits the game framerate to 60fps
    clock.tick(60)

pygame.quit()