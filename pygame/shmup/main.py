# pygame shmup game
# this is the main file for this program

#modules-------------------------------------------------------------------------------------------
import pygame, random
from pathlib import Path
import game_loop, menus
from config import *
from assets import *
from classes import *



#pygame init---------------------------------------------------------------------------------------
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(ssize)
pygame.display.set_caption("Shmup")
clock = pygame.time.Clock()


# different loops
loops = {"game" : game_loop.run_game, "start" : menus.run_start}

loop_history = ["game"] # stores history of which game loop which was in action

# loop setup
running = True
# game loop----------------------------------------------------------------------------------------
while running:
    # timing
    clock.tick(fps)

    feedback = loops[loop_history[-1]](screen)
    for request in feedback:
        if request[:7] == "switch:":
            destination = request[7:]
            if destination in loops.keys():
                loop_history.append(destination)


    pygame.display.flip()

pygame.quit()
