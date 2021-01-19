# sprite classes for tile game
# modules
from settings import *
import pygame as pg
from pathlib import Path
import random
import math

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game

        self.image = self.game.player_img

        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0, 0)


    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x -= 1
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x += 1
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y -= 1
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y += 1

        if self.vel:
            self.vel = self.vel.normalize()
        self.vel *= PLAYER_SPEED


    def collide_with_walls(self):
        # overcomplicated collisions to remove wierd snaping
        # - no dependency on velocities
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        for hit in hits:
            offset = hit.pos - self.pos
            col_angle = offset.as_polar()[1] # angle anticlockwise

            if 137 < abs(col_angle):
                # wall on right
                self.vel.x = max(0, self.vel.x)
                self.pos.x += 0.5/tsize[0]

            elif 47 < col_angle < 133:
                # wall on above
                self.vel.y = min(0, self.vel.y)
                self.pos.y -= 0.5/tsize[1]

            elif -43 < col_angle < 43:
                # wall on left
                self.vel.x = min(0, self.vel.x)
                self.pos.x -= 0.5/tsize[0]

            elif -133 < col_angle < -47:
                # wall below
                self.vel.y = max(0, self.vel.y)
                self.pos.y += 0.5/tsize[1]


    def update(self):
        # movement
        self.get_keys()
        self.collide_with_walls()
        self.pos += self.vel * self.game.dt
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
