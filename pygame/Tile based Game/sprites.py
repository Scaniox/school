# sprite classes for plaform game
#modules
from settings import *
import pygame as pg
from pathlib import Path
import xml.etree.ElementTree as ET
import random

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game

        self.image = pg.Surface(tsize)
        self.image.fill((255,255,0))

        self.rect = self.image.get_rect()
        self.pos = vec(x, y)


    def collide_with_walls(self, dpos=[0,0]):
        # checks if there is a wall at pos + dpos
        for wall in self.game.walls:
            if wall.pos == self.pos + vec(dpos):
                return True
        return False


    def move(self, dpos=[0,0]):
        # try to move 
        if not self.collide_with_walls(dpos):
            self.pos += vec(dpos)


    def update(self):
        self.rect.topleft = [self.pos[i] * tsize[i] for i in [0,1]]



class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        super().__init__(self.groups)
        self.game = game

        self.image = pg.Surface(tsize)
        self.image.fill((0,255,0))

        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.topleft = [self.pos[i] * tsize[i] for i in [0,1]]
