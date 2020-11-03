# pygame shmup game
# this is the main file for this program

#modules-------------------------------------------------------------------------------------------
import pygame, random
from pathlib import Path

#constants-----------------------------------------------------------------------------------------
ssize = (480,600)
fps = 60

img_dir = Path(__file__).parent / "img"

#variables-----------------------------------------------------------------------------------------

#functions-----------------------------------------------------------------------------------------

#pygame init---------------------------------------------------------------------------------------
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(ssize)
pygame.display.set_caption("Shmup")

#classes-------------------------------------------------------------------------------------------

# player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
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

    def update(self):
        keys = pygame.key.get_pressed()
        # arrows to change velocity
        if keys[pygame.K_LEFT]:
            self.velocity[0] -= 1
        elif keys[pygame.K_RIGHT]:
            self.velocity[0] += 1

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


    # fire a bullet
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


# enemy sprites
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.respawn()
        self.rot = 0
        self.rot_velocity = random.random()*8-4
        self.last_update = pygame.time.get_ticks()

        # collision data
        self.radius = self.rect.width//2.2


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
        self.original_image.set_colorkey((0,0,0))
        self.image = self.original_image.copy()

        # sprite movement
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ssize[0]- self.rect.width)
        self.rect.y = random.randint(-150, -100)
        self.velocity = [random.random()*4-2,\
                      random.random()*5+1]


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



#object inits--------------------------------------------------------------------------------------
#¬ image asset init
background_img = pygame.image.load(str(img_dir / "background_blue.png")).convert()
scaled_background = pygame.transform.scale(background_img, ssize)

player_img = pygame.image.load(str(img_dir / "playerShip1_blue.png")).convert()
bullet_img = pygame.image.load(str(img_dir / "laserBlue01.png")).convert()

#¬¬ load all images in Meteors folder
meteor_imgs = []
for image in (img_dir / "Meteors").iterdir():
    meteor_imgs.append(pygame.image.load(str(image)).convert())


#¬ group generation
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

#¬ generate player
player = Player()
all_sprites.add(player)

#¬ generate mobs
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# loop setup
running = True
# game loop----------------------------------------------------------------------------------------
while running:
    # timing#
    clock.tick(fps)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        # shoot
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # update
    all_sprites.update()

    #collisions
    #¬ bullet - mob collision
    hits = pygame.sprite.groupcollide(mobs, bullets, False, True)
    for hit_mob in hits:
        hit_mob.respawn()

    #¬ mob - player collision
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    if hits:
        running = False

    # display
    screen.blit(scaled_background, [0,0])
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
