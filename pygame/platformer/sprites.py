# sprite classes for plaform game
#modules
from settings import *
import pygame as pg
from pathlib import Path
import xml.etree.ElementTree as ET
from random import choice, randint

vec = pg.math.Vector2

class Spritesheet():
    #utility class for loading and parsing spritesheets
    def __init__(self, file_name):
        self.spritesheet = pg.image.load(file_name).convert()

        # load and parse xml file
        self.xml_tree = ET.parse(str(Path(f"{file_name[:-3]}xml")))

    def get_image(self, name):
        # returns an image from the spritesheet using the xml to find it
        try:
            sprite_entry = self.xml_tree.getroot().find(f"SubTexture[@name='{name}']")
        except Exception as error:
            print(f"failed to find data for {name} in xml file because of error: {error}")
            exit()

        sprite_rect = [int(sprite_entry.get(f"{i}")) for i in ["x","y","width","height"]]

        output_surface = pg.surface.Surface(sprite_rect[2:])
        output_surface.set_colorkey((0,0,0))
        output_surface.blit(self.spritesheet, (0, 0), sprite_rect)

        return output_surface


class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = [game.all_sprites]
        super().__init__(self.groups)
        self.game = game
        # animation
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()
        # image
        self.load_images()
        self.image = self.standing_frames[0]
        # rect
        self.rect = self.image.get_rect()
        self.rect.center = [i//2 for i in ssize]
        self.pos = vec(40, ssize[1] - 100)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def load_images(self):
        # load
        self.standing_frames = [self.game.spritesheet.get_image("bunny1_ready.png"),
                                self.game.spritesheet.get_image("bunny1_stand.png")]
        self.walking_frames_r = [  self.game.spritesheet.get_image("bunny1_walk1.png"),
                                self.game.spritesheet.get_image("bunny1_walk2.png")]
        # scale
        self.standing_frames = [pg.transform.scale(image, [i//2 for i in image.get_size()]) for image in self.standing_frames]
        self.walking_frames_r = [pg.transform.scale(image, [i//2 for i in image.get_size()]) for image in self.walking_frames_r]

        self.walking_frames_l = [pg.transform.flip(image, True, False) for image in self.walking_frames_r]

        self.jump_frame = self.game.spritesheet.get_image("bunny1_jump.png")

    def jump(self):
        self.rect.y += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2

        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP_STRENGTH

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
                self.jumping = False

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)

        # = key presses
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.acc.x = - PLAYER_ACC

        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # kinematics
        self.acc.x += self.vel.x * PLAYER_FRICTION  # friction
        self.vel += self.acc                    # velocity
        self.pos += self.vel + 0.5 * self.acc   # displacement
        image_size = self.image.get_size()

        # sceen edge wraparound
        if self.pos.x < 0 - image_size[0] // 2:
            self.pos.x = ssize[0] + image_size[0] // 2
        elif self.pos.x > ssize[0] + image_size[0] // 2:
            self.pos.x = 0 - image_size[0] // 2

        self.rect.midbottom = self.pos

    def animate(self):
        now = pg.time.get_ticks()
        self.walking = round(self.vel.x) != 0

        # standing animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 300:
                self.last_update = now

                bottom = self.rect.bottom
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # walking animation
        if self.walking:
            # faster vel.x = faster animation
            if now - self.last_update > 300/max(abs(self.vel.x), 10**-6):
                self.last_update = now

                bottom = self.rect.bottom
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                # select which direction to use
                if self.vel.x > 0:
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_frames_l[self.current_frame]

                self.rect = self.image.get_rect()
                self.rect.bottom = bottom


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.platforms

        super().__init__(self.groups)
        self.game = game
        images = [  self.game.spritesheet.get_image("ground_grass.png"),
                    self.game.spritesheet.get_image("ground_grass_small.png")]
        images = [pg.transform.scale(img, [dim//2 for dim in img.get_size()]) for img in images]

        self.image = choice(images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        if randint(0,100) < POW_SPAWN_PCT:
            Power_up(self.game, self)


class Power_up(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self.groups = game.all_sprites, game.powerups

        super().__init__(self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(["boost"])

        image = self.game.spritesheet.get_image("powerup_jetpack.png")
        self.image = pg.transform.scale(image, [dim//2 for dim in image.get_size()])

        self.rect = self.image.get_rect()
        self.rect.x = self.plat.rect.x
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        if self.game.platforms.has(self.plat):
            self.rect.bottom = self.plat.rect.top - 5
        else:
            self.kill()
