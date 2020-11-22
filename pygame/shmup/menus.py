# this file contains the menu navigation loop code
import pygame, random
from config import *
from assets import *
from classes import *

last_pause_time = pygame.time.get_ticks()


class start_menu():
    def __init__(self):
        self.last__loop = 0


    def run(self, screen, loop_history):
        # list of arguments to feed back to controller
        feedback = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                feedback.append("exit")
            if event.type == pygame.KEYDOWN:
                feedback.append("switch:game")

        screen.blit(scaled_background, [0,0])
        draw_text(screen, "SHMUP!", (200,200,200), 60, [ssize[0]//2, ssize[1]//4] )
        draw_text(screen, "press any key to start", (200,200,200), 24, [ssize[0]//2, ssize[1]//2])
        pygame.display.flip()

        return feedback



# pause menu
class pause_menu():
    def __init__(self):
        self.last_loop = 0
        self.game_image = scaled_background

        center = [i//2 for i in ssize]
        self.resume_rect = pygame.rect.Rect([center[0]-100, center[1]-70, 200, 40])
        self.exit_rect = pygame.rect.Rect([center[0]-100, center[1]-20, 200, 40])


    def run(self, screen, loop_history):
        # list of arguments to feed back to controller
        feedback = []

        #run when switching to this one
        if pygame.time.get_ticks() - self.last_loop > 50:
            self.game_image = screen


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                feedback.append("exit")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    feedback.append("switch:game")

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if self.resume_rect.collidepoint(mouse_pos):
                    feedback.append("switch:game")

                if self.exit_rect.collidepoint(mouse_pos):
                    feedback.append("switch:start")


        screen.blit(self.game_image, [0,0])
        draw_text(screen, "PAUSED", (200,200,200), 60, [ssize[0]//2, ssize[1]//4])
        #resume button
        pygame.draw.rect(screen, (20,20,150), self.resume_rect)
        pygame.draw.rect(screen, (200,200,200), self.resume_rect, 2)
        draw_text(screen, "Resume", (150,150,150), 24, self.resume_rect.center)
        #exit button
        pygame.draw.rect(screen, (20,20,150), self.exit_rect)
        pygame.draw.rect(screen, (200,200,200), self.exit_rect, 2)
        draw_text(screen, "Exit", (150,150,150), 24, self.exit_rect.center)

        pygame.display.flip()

        self.last_loop = pygame.time.get_ticks()

        return feedback
