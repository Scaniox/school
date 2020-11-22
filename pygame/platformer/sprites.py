# sprite classes for plaform game
#modules
from settings import *
import pygame as pg

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.image = pg.Surface((30,40))
        self.image.fill((255,255,0))
        self.rect = self.image.get_rect()
        self.rect.center = [i//2 for i in ssize]
        self.pos = vec([i//2 for i in ssize])
        self.vel = vec(0,0)
        self.acc = vec(0,0)


    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 1

        if hits:
            self.vel.y = -player_jump_strength



    def update(self):
        self.acc = vec(0,player_grav)

        # = key presses
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.acc.x = -player_acc

        if keys[pg.K_RIGHT]:
            self.acc.x = player_acc

        # kinematics
        self.acc.x += self.vel.x * player_friction  # friction
        self.vel += self.acc                    # velocity
        self.pos += self.vel + 0.5 * self.acc   # displacement
        self.pos.x %= ssize[0]

        self.rect.midbottom = self.pos


class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pg.Surface((w,h))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
