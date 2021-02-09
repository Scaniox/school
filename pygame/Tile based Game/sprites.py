# sprite classes for tile game
# modules
from settings import *
import pygame as pg
from pathlib import Path
import random
import math
import pytweening as tween
import itertools

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
        if sprite.hit_rect.x+5 > hit.rect.right:
            # wall on left
            sprite.vel.x = max(0, sprite.vel.x)
            sprite.vel.y *= wall_drag

        elif sprite.hit_rect.bottom-5 < hit.rect.y:
            # wall below
            sprite.vel.y = min(0, sprite.vel.y)
            sprite.vel.x *= wall_drag

        elif sprite.hit_rect.right-5 < hit.rect.x:
            # wall on right
            sprite.vel.x = min(0, sprite.vel.x)
            sprite.vel.y *= wall_drag

        elif sprite.hit_rect.y+5 > hit.rect.bottom:
            # wall above
            sprite.vel.y = max(0, sprite.vel.y)
            sprite.vel.x *= wall_drag



class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
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
        self.weapon = "pistol"
        self.damaged = False


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
            self.shoot()

        if self.acc:
            self.acc = self.acc.normalize()

        self.acc *= PLAYER_SPEED
        self.rot_speed *= PLAYER_ROT_SPEED

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]["rate"]:
            self.last_shot = now
            pos = self.rect.center + vec(WEAPONS[self.weapon]["barrel_offset"]).rotate(-self.rot)
            for shot in range(WEAPONS[self.weapon]["bullet_count"]):
                dir = vec(1,0).rotate(-self.rot + random.uniform(-WEAPONS[self.weapon]["spread"], WEAPONS[self.weapon]["spread"]))
                Bullet(self.game, pos, dir * WEAPONS[self.weapon]["bullet_speed"], WEAPONS[self.weapon]["damage"])

            #kickback
            self.vel -= vec(WEAPONS[self.weapon]["kickback"], 0).rotate(-self.rot)
            # muzzle flash
            Muzzle_flash(self.game, pos)
            # sound
            random.choice(self.game.weapon_sounds[self.weapon]).play()


    def hit(self):
        self.damaged = True
        self.damage_alpha = itertools.chain(DAMAGE_ALPHA)

    def update(self):
        # movement
        self.get_keys()
        self.acc -= self.vel * PLAYER_DRAG
        self.vel += self.acc * self.game.dt
        collide_with_group(self, self.game.walls, col_funct=collide_hit_rect, wall_drag=WALL_DRAG)
        self.pos += self.vel * self.game.dt
        self.rot = self.rot + (self.rot_speed * self.game.dt) % 360

        self.rect.center = [(self.pos[i]+0.5) * tsize[i] for i in [0,1]]
        self.hit_rect.center = self.rect.center

        old_center = self.rect.center
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        # damage flashing effect
        if self.damaged:
            try:
                self.image.fill((255,100,100, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False

        self.rect = self.image.get_rect()
        self.rect.center = old_center


    def add_health(self, amount):
        self.health = min(self.health + amount, PLAYER_HEALTH)



class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = [game.all_sprites, game.mobs]
        super().__init__(self.groups)
        self.game = game

        self.image = self.game.mob_img.copy()

        self.pos = vec(x, y)
        self.acc = vec(0, 0)
        self.vel = vec(0, 0)
        self.rot = 0
        self.rect = self.image.get_rect()
        self.rect.center = [(self.pos[i]+0.5) * tsize[i]+0.5 for i in [0,1]]
        self.hit_rect = MOB_HIT_RECT.copy()

        self.health = MOB_HEALTH
        self.speed = MOB_SPEED + random.uniform(-MOB_SPEED_UNCERTAINTY, MOB_SPEED_UNCERTAINTY)
        self.target = game.player


    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize() * DISTANCING_FORCE


    def update(self):
        self.acc = vec(0, 0)

        target_dist = self.target.pos - self.pos
        # chasing player
        if target_dist.length_squared() < DETECT_RADIUS**2:
            if random.random() < 0.002:
                random.choice(self.game.zombie_moan_sounds).play()

            # rotate
            self.rot = target_dist.angle_to((1,0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)

            # acceleration
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc -= self.vel * MOB_DRAG

        # move
        try:
            self.acc.scale_to_length(self.speed)
        except Exception as e:
            pass
            
        self.vel += self.acc * self.game.dt
        collide_with_group(self, self.game.walls, col_funct = collide_hit_rect)
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
            random.choice(self.game.zombie_hit_sounds).play()
            self.game.map_img.blit(self.game.splat, self.rect.topleft)


    def draw_health(self):
        col = (0,255,0) if self.health > 60 else (255,255,0) if self.health > 30 else (255,0,0)

        width = int(self.rect.width * (self.health / MOB_HEALTH))
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)



class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):
        self._layer = BULLET_LAYER
        self.game = game
        self.groups = [game.all_sprites, game.bullets]
        self.image = self.game.bullet_imgs[WEAPONS[self.game.player.weapon]["bullet_size"]]
        super().__init__(self.groups)

        self.pos = vec(pos)
        self.dir = dir * random.uniform(0.9, 1.1)
        self.damage = damage

        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.rect.center = self.pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.dir * self.game.dt
        self.rect.center = self.pos

        # deleting bullets
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if self.spawn_time + WEAPONS[self.game.player.weapon]["bullet_lifetime"] < pg.time.get_ticks():
            self.kill()



class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
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



class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = [game.walls]
        super().__init__(self.groups)
        self.game = game

        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect



class Muzzle_flash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game

        size = random.randint(20,50)
        self.image = pg.transform.scale(random.choice(self.game.gun_flashes), [size]*2)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = self.pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if self.spawn_time + FLASH_DURATION < pg.time.get_ticks():
            self.kill()



class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER
        self.groups = [game.all_sprites, game.items]
        super().__init__(self.groups)
        self.game = game
        self.image = self.game.item_imgs[type]

        self.pos = vec(pos)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.type = type

        self.tween = tween.easeInOutSine
        self.step = 0 # how far into the tween function
        self.dir = 1

    def update(self):
        # bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        # reversing direction
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1
