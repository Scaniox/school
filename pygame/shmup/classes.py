# this file contains the classes

import pygame, random
from pathlib import Path
from config import *
from assets import *

#classes-------------------------------------------------------------------------------------------

# player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__()
        self.groups = groups
        # sprite image
        self.image = pygame.transform.scale(player_img, [50,38])
        self.image.set_colorkey((0,0,0))

        # sprite movement
        self.rect = self.image.get_rect()
        self.rect.centerx = ssize[0] // 2
        self.rect.bottom = ssize[1]-10
        self.velocity = [0,0]
        # collision data
        self.radius = 20

        # game attributes
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.shield = 100
        self.shoot_delay = 200
        self.last_shoot = pygame.time.get_ticks()

        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()

        # unhide
        if self.hidden and pygame.time.get_ticks() > self.hide_timer + 1000:
            self.hidden = False
            self.rect.midbottom = [ssize[0]//2 , ssize[1] - 10]
            print("unhide")

        # reduce power level
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > powerup_time:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        # arrows to change velocity
        if keys[pygame.K_LEFT]:
            self.velocity[0] -= 1
        elif keys[pygame.K_RIGHT]:
            self.velocity[0] += 1

        # shooting
        if keys[pygame.K_SPACE]:
            if pygame.time.get_ticks() > self.last_shoot + self.shoot_delay:
                self.shoot()
                self.last_shoot = pygame.time.get_ticks()
        else:
            self.last_shoot = 0

        # move sprite
        for i in [0,1]:
            self.rect[i] = round(self.rect[i] + self.velocity[i])
            # friction
            self.velocity[i] *= 0.9

        # off left side of screen check
        if self.rect.left < 0:
            self.rect.left = 0
            self.velocity[0] = 0

        # off right side of screen check
        elif self.rect.right > ssize[0]:
            self.rect.right = ssize[0]
            self.velocity[0] = 0

    # get a power up
    def powerup(self):
        self.power = min(self.power+1, 2)
        self.power_time = pygame.time.get_ticks()


    # fire a bullet
    def shoot(self):
        now = pygame.time.get_ticks()
        if self.power == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.groups["all_sprites"].add(bullet)
            self.groups["bullets"].add(bullet)
            shoot_sound.play()

        elif self.power == 2:
            bullet_L = Bullet(self.rect.left, self.rect.centery)
            bullet_R = Bullet(self.rect.right, self.rect.centery)
            self.groups["all_sprites"].add(bullet_L, bullet_R)
            self.groups["bullets"].add(bullet_L, bullet_R)
            shoot_sound.play()


    # temporarily hide the player
    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (ssize[0]//2, ssize[1]+200 )


# enemy sprites
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.respawn()
        self.last_update = pygame.time.get_ticks()

        # collision data
        self.radius = ((self.rect.width**2)+(self.rect.height**2))**(1/2)//2


    def update(self):
        # move
        for i in [0,1]:
            self.rect[i] += self.velocity[i]

        # rotation
        now = pygame.time.get_ticks()
        if now - self.last_update > 10:
            self.last_update = now

            self.rot = (self.rot + self.rot_velocity) % 360
            new_image = pygame.transform.rotate(self.original_image, self.rot)
            # handle rect changes
            old_center = self.rect.center
            self.image = new_image
            self.image.set_colorkey((0,0,0))
            self.rect = self.image.get_rect()
            self.rect.center = old_center


        # respawn if off screen
        if self.rect.top > ssize[1] or \
           self.rect.right < 0 or \
           self.rect.left > ssize[0]:
            self.respawn()


    def respawn(self):
        # sprite image
        self.original_image = random.choice(meteor_imgs)
        self.image = self.original_image.copy()

        # sprite movement
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ssize[0]- self.rect.width)
        self.rect.y = 50 #random.randint(-150, -100)
        self.velocity = [random.random()*2-1,\
                      random.random()*5+1]
        # rotations
        self.rot = 0
        self.rot_velocity = random.random()*8-4


# bullet sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # sprite image
        self.image = bullet_img
        self.image.set_colorkey((0,0,0))

        # sprite movement
        self.rect = self.image.get_rect()
        self.rect.midbottom = [x,y]
        self.velocity = [0,-10]

    def update(self):
        # update position
        for i in [0,1]:
            self.rect[i] += self.velocity[i]

        # remove if off screen
        if self.rect.bottom < 0:
            self.kill()


# explosion sprite
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_delay = 50

    def update(self):
        now = pygame.time.get_ticks()
        if pygame.time.get_ticks() > self.last_update + self.frame_delay:
            self.last_update = now
            self.frame +=1

            if self.frame == len(expl_anim[self.size]):# remove if at end of frames
                self.kill()

            else: # next frame
                center = self.rect.center
                self.image = expl_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# power ups
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.type = random.choice(["shield", "gun"])
        # sprite image
        self.image = powerup_images[self.type]
        self.image.set_colorkey((0,0,0))

        # sprite movement
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.velocity = [0,5]

    def update(self):
        # update position
        for i in [0,1]:
            self.rect[i] += self.velocity[i]

        # remove if off screen
        if not screen_rect.contains(self.rect):
            self.kill()
