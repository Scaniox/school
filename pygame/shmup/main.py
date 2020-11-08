# pygame shmup game
# this is the main file for this program

#modules-------------------------------------------------------------------------------------------
import pygame, random
from pathlib import Path

#constants-----------------------------------------------------------------------------------------
ssize = (480,600)
fps = 60

img_dir = Path(__file__).parent / "img"
snd_dir = Path(__file__).parent / "snd"

font_arial = pygame.font.match_font("arial")

#variables-----------------------------------------------------------------------------------------
score = 0

#functions-----------------------------------------------------------------------------------------
# generate text at position on screen
def draw_text(surface, text, colour, size, rect):
    font = pygame.font.Font(font_arial, size)
    text_surf = font.render(text, True, colour)

    text_rect = text_surf.get_rect()
    text_rect.topleft = rect
    surface.blit(text_surf, rect)


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

        # game attributes
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.shield = 100
        self.shoot_delay = 200
        self.last_shoot = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()

        # unhide
        if self.hidden and pygame.time.get_ticks() > self.hide_timer + 1000:
            self.hidden = False
            self.rect.midbottom = [ssize[0]//2 , ssize[1] - 10]
            print("unhide")

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


    # fire a bullet
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
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
        self.rot = 0
        self.rot_velocity = random.random()*8-4
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

#object inits--------------------------------------------------------------------------------------
#¬ image asset init
background_img = pygame.image.load(str(img_dir / "background_blue.png")).convert()
scaled_background = pygame.transform.scale(background_img, ssize)

player_img = pygame.image.load(str(img_dir / "playerShip1_blue.png")).convert()
player_live_img = pygame.transform.scale(player_img.copy(), (25,19))
player_live_img.set_colorkey((0,0,0))
bullet_img = pygame.image.load(str(img_dir / "laserBlue01.png")).convert()

#¬¬ load all images in Meteors folder
meteor_imgs = []
for image in (img_dir / "Meteors").iterdir():
    meteor_imgs.append(pygame.image.load(str(image)).convert())

#¬¬ explosion images
expl_anim = {}
expl_anim["S"] = []
expl_anim["L"] = []
expl_anim["P"] = []

for i in range(9):
    img = pygame.image.load(str(img_dir / "explosions" / f"regularExplosion0{i}.png")).convert()
    img.set_colorkey((0,0,0))
    expl_anim["L"].append(pygame.transform.scale(img, (75,75)))
    expl_anim["S"].append(pygame.transform.scale(img, (32,32)))

    img = pygame.image.load(str(img_dir / "explosions" / f"sonicExplosion0{i}.png")).convert()
    img.set_colorkey((0,0,0))
    expl_anim["P"].append(pygame.transform.scale(img, (150,150)))

#¬ sound asset init
shoot_sound = pygame.mixer.Sound(str(snd_dir / "shoot.wav"))
die_sound = pygame.mixer.Sound(str(snd_dir / "ship explosion.wav"))
#¬¬ meteor explosion sounds
meteor_expl_snd = [pygame.mixer.Sound(str(snd_dir / name)) for name in ["Explosion.wav","Explosion2.wav"]]

#¬¬ background music
"""pygame.mixer.music.load(str(snd_dir / "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()"""


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

    # update
    all_sprites.update()

    #collisions
    #¬ bullet - mob collision
    hits = pygame.sprite.groupcollide(mobs, bullets, False, True)
    for hit_mob in hits:
        score += round(100 - hit_mob.radius)

        expl = Explosion(hit_mob.rect.center, "L")
        all_sprites.add(expl)

        random.choice(meteor_expl_snd).play()

        hit_mob.respawn()

    #¬ mob - player collision
    hits = pygame.sprite.spritecollide(player, mobs, False, pygame.sprite.collide_circle)
    for hit_mob in hits:
        player.shield -= hit_mob.radius

        if player.shield <= 0: # cause player death
            death_expl = Explosion(player.rect.center, "P")
            all_sprites.add(death_expl)
            die_sound.play()
            player.hide()
            player.lives -= 1
            player.shield = 100

        expl = Explosion(hit_mob.rect.center, "S")
        all_sprites.add(expl)
        hit_mob.respawn()

    if player.lives == 0 and not death_expl.alive():
        running = False

    # display
    screen.blit(scaled_background, [0,0])
    all_sprites.draw(screen)

    draw_text(screen, str(score), (200,200,0), 28, (ssize[0]//2, 10))
    draw_bar(screen, [5,5], player.shield)
    draw_lives(screen, [ssize[0]-100, 10], player.lives, player_live_img)

    pygame.display.flip()

pygame.quit()
