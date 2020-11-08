# this file contains data about the game that doesn't change
import pygame
from pathlib import Path

ssize = (480,600)
screen_rect = pygame.Rect(0, 0, *ssize)
fps = 60

img_dir = Path(__file__).parent / "img"
snd_dir = Path(__file__).parent / "snd"

font_arial = pygame.font.match_font("arial")
powerup_time = 10000




# functions ---------------------------------------------------------------------------------------
# generate text at position on screen
def draw_text(surface, text, colour, size, rect):
    font = pygame.font.Font(font_arial, size)
    text_surf = font.render(text, True, colour)

    text_rect = text_surf.get_rect()
    text_rect.center = rect
    surface.blit(text_surf, text_rect)


# generate bar to show a percentage
def draw_bar(surface, pos, pct):
    pct = max(pct, 0)
    bar_size = [100,10]
    fill_length = (pct/100) * bar_size[0]
    outline_rect = pygame.Rect(*pos, *bar_size)
    fill_rect = pygame.Rect(*pos, fill_length, bar_size[1])

    pygame.draw.rect(surface, (50,50,50), outline_rect)
    pygame.draw.rect(surface, (0,255,0), fill_rect)
    pygame.draw.rect(surface, (200,200,200), outline_rect, 2)


def draw_lives(surface, pos, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = pos[0] + 30*i
        img_rect.y = pos[1]

        surface.blit(img, img_rect)
