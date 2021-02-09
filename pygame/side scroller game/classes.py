import pygame as pg
from functions import *
import config as cfg

vec2 = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.game = game
        self.groups = [self.game.draw_sprites, self.game.update_sprites]
        super().__init__(self.groups)

        self.pos = vec2(pos) * cfg.tsize
        self.vel = vec2(0, 0)
        self.acc = vec2(0, cfg.grav)

        self.image = self.game.player_img.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.colliding = False
        self.last_jump = pg.time.get_ticks()


    def keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            self.acc.x -= cfg.player_acc
        elif keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.acc.x += cfg.player_acc
        if keys[pg.K_SPACE] and self.colliding and self.last_jump + 100 < pg.time.get_ticks():
            self.last_jump = pg.time.get_ticks()
            self.vel.y -= cfg.jump_power


    def collision_vel_cancel_old(self):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        for block in hits:

            # block below
            if block.rect.top >= self.rect.bottom-10:
                print("below")
                self.vel.y = min(0, self.vel.y)
            # block above
            elif self.rect.top+10 >= block.rect.bottom:
                print("above")
                self.vel.y = max(0, self.vel.y)

            # block right
            if block.rect.left >= self.rect.right-10:
                print("right")
                self.vel.x = min(0, self.vel.x)
            # block left
            elif self.rect.left+10 >= block.rect.right:
                print("left")
                self.vel.x = max(0, self.vel.x)

        if hits:
            self.colliding = True
        else:
            self.colliding = False

    def collision_vel_cancel(self):
        self.colliding = False
        for offset in [(0,1,"top","bottom"), (0,-1,"bottom","top"), (1,0,"right","left"), (-1,0,"right","left")]:
            self.rect.center += vec2(offset[:2])
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            self.rect.center -= vec2(offset[:2])
            self.colliding |= bool(hits)
            if hits:
                print(offset[2])

            for block in hits:
                self.rect.__setattr__(offset[2], block.rect.__getattribute__(offset[3]))
                if abs(offset[0]): # x collisions
                    self.vel.x = 0
                else:              # y collsions
                    self.vel.y = 0


    def update(self):
        self.acc = vec2(0, cfg.grav)
        self.keys()
        self.vel += self.acc * self.game.dt
        self.collision_vel_cancel()
        if self.colliding:
            self.vel.x *= cfg.friction
        self.pos += self.vel * self.game.dt

        self.rect.topleft = vec2(self.pos)



class Block(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.game = game
        self.groups = [self.game.draw_sprites, self.game.update_sprites, self.game.walls]
        super().__init__(self.groups)

        self.image = self.game.wall_img
        self.image = pg.transform.scale(self.image, [cfg.tsize]*2)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos * cfg.tsize



class Flag(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self.game = game
        self.groups = [self.game.draw_sprites, self.game.update_sprites]
        super().__init__(self.groups)

        self.image = self.game.flag_imgs[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos * cfg.tsize
        self.raised = False


    def activate(self):
        self.raised = True
        self.image = self.game.flag_imgs[1]
        pos = self.rect.topleft
        self.rect = self.image.get_rect()
        self.rect.topleft = pos



class Camera(pg.sprite.Sprite):
    def __init__(self, game, target):
        self.game = game
        self.groups = [self.game.update_sprites]
        super().__init__(self.groups)

        self.target = target
        self.pos = vec2(target.rect.center)


    def transform_rect(self, rect):
        return rect.move(self.pos)


    def update(self):
        self.pos.x = -max(0, min((self.game.bsize[0])*cfg.tsize - cfg.ssize[0], self.target.rect.centerx - cfg.ssize[0] // 2))
        self.pos.y = -max(0, min((self.game.bsize[1])*cfg.tsize - cfg.ssize[1], self.target.rect.centery - cfg.ssize[1] // 2))
