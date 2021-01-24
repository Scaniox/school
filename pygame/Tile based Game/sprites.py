# sprite classes for tile game
# modules
from settings import *
import pygame as pg
from pathlib import Path
import random
import math

vec = pg.math.Vector2

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def collide_with_group(sprite, other_group, col_funct=False, wall_drag=1):
    # overcomplicated collisions to remove wierd snapping
    # - no dependency on velocities, which can cause problems
    if col_funct:
        hits = pg.sprite.spritecollide(sprite, other_group, False, col_funct)
    else:
        hits = pg.sprite.spritecollide(sprite, other_group, False )

    for hit in hits:
        offset = hit.pos - sprite.pos
        col_angle = -offset.angle_to((1,0)) # angle anticlockwise

        if 135 <= abs(col_angle) and hit.exposed_edges["R"]:
            # wall on left
            sprite.vel.x = max(0, sprite.vel.x)
            sprite.vel.y *= wall_drag

        if 45 <= col_angle <= 135 and hit.exposed_edges["U"]:
            # wall below
            sprite.vel.y = min(0, sprite.vel.y)
            sprite.vel.x *= wall_drag

        if -45 <= col_angle <= 45 and hit.exposed_edges["L"]:
            # wall on right
            sprite.vel.x = min(0, sprite.vel.x)
            sprite.vel.y *= wall_drag

        if -135 <= col_angle <= -45 and hit.exposed_edges["D"]:
            # wall above
            sprite.vel.y = max(0, sprite.vel.y)
            sprite.vel.x *= wall_drag



class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = [game.all_sprites]
        super().__init__(self.groups)
        self.game = game

        self.image = self.game.player_img

        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0

        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.rect.center = [(self.pos[i]+0.5) * tsize[i]+0.5 for i in [0,1]]

        self.health = PLAYER_HEALTH
        self.last_shot = 0


    def get_keys(self):
        self.rot_speed = 0
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed += 1
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed -= 1

        if keys[pg.K_UP] or keys[pg.K_w]:
            self.acc += vec(1,0).rotate(-self.rot)
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            self.acc -= vec(0.5,0).rotate(-self.rot)

        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1,0).rotate(-self.rot + random.uniform(-GUN_SPREAD, GUN_SPREAD))
                pos = self.rect.center + vec(BARREL_OFFSET).rotate(-self.rot)
                Bullet(self.game, pos, dir)
                #kickback
                self.vel -= vec(KICKBACK, 0).rotate(-self.rot)


        if self.acc:
            self.acc = self.acc.normalize()

        self.acc *= PLAYER_SPEED
        self.rot_speed *= PLAYER_ROT_SPEED


    def update(self):
        # movement
        self.get_keys()
        collide_with_group(self, self.game.walls, col_funct=collide_hit_rect, wall_drag=WALL_DRAG)
        self.acc -= self.vel * PLAYER_DRAG
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt
        self.rot = self.rot + (self.rot_speed * self.game.dt) % 360

        self.rect.center = [(self.pos[i]+0.5) * tsize[i] for i in [0,1]]
        self.hit_rect.center = self.rect.center

        old_center = self.rect.center
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = old_center



class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = [game.all_sprites, game.mobs]
        super().__init__(self.groups)
        self.game = game

        self.image = self.game.mob_img

        self.pos = vec(x, y)

        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.rot = 0
        self.rect = self.image.get_rect()
        self.rect.center = [(self.pos[i]+0.5) * tsize[i]+0.5 for i in [0,1]]
        self.hit_rect = MOB_HIT_RECT.copy()

        self.health = MOB_HEALTH

    def update(self):
        # rotate
        self.rot = (self.game.player.pos - self.pos).angle_to((1,0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        # move
        self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
        self.acc -= self.vel * MOB_DRAG
        collide_with_group(self, self.game.walls, col_funct = collide_hit_rect)
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt

        # update rect
        self.rect = self.image.get_rect()
        self.rect.center = [(self.pos[i]+0.5) * tsize[i] for i in [0,1]]
        self.hit_rect.center = self.rect.center

        # rotate image
        old_center = self.rect.center
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = old_center

        # death
        if self.health <= 0:
            self.kill()


    def draw_health(self):
        col = (0,255,0) if self.health > 60 else (255,255,0) if self.health > 30 else (255,0,0)

        width = int(self.rect.width * (self.health / MOB_HEALTH))
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir):
        self.game = game
        self.groups = [game.all_sprites, game.bullets]
        super().__init__(self.groups)
        self.image = pg.transform.scale(game.bullet_img, [i//2 for i in self.game.bullet_img.get_size()])

        self.pos = pos
        self.dir = dir.normalize()

        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.start_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.dir * BULLET_SPEED * self.game.dt
        self.rect.center = self.pos

        # deleting bullets
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if self.start_time + BULLET_LIFETIME < pg.time.get_ticks():
            self.kill()



class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = [game.all_sprites, game.walls]
        super().__init__(self.groups)
        self.game = game

        self.image = pg.transform.scale(game.wall_img, tsize)

        self.colliding = False
        self.exposed_edges = {"U": True, # which edges are collidable
                              "R": True,
                              "D": True,
                              "L": True}
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.topleft = [self.pos[i] * tsize[i] for i in [0,1]]
