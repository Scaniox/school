# pygame skeleton template

#modules---------------------------------------------------------------------------
import pygames

#constants
ssize = (800,600)
fps = 30

#variables

#functions

#classes

#object inits
clock = pygame.time.Clock()

#pygame init
pygame.init()
screen = pygame.display.set_mode(ssize)
pygame.display.set_caption("game name")

# loop setup
running = True
# game loop
while running:
    # timing#
    clock.tick(fps)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

    # update

    # display
    screen.fill((255,255,255))

    pygame.display.flip()

pygame.quit()
