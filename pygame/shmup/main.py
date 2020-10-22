# pygame skeleton template

#modules---------------------------------------------------------------------------
import pygame, random

#constants
ssize = (480,600)
fps = 60

#variables

#functions

#pygame init
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(ssize)
pygame.display.set_caption("Shmup")

#classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.surface.Surface((50,50))
        self.image.fill((0,255,0))

        self.rect = self.image.get_rect()
        self.rect.centerx = ssize[0] // 2
        self.rect.bottom = ssize[1]-10
        self.speed = [0,0]

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed[0] -= 1
        elif keys[pygame.K_RIGHT]:
            self.speed[0] += 1

        for i in [0,1]:
            self.rect[i] += self.speed[i]

        if self.rect.left < 0:
            self.rect.left = 0
            self.speed[0] = 0

        elif self.rect.right > ssize[0]:
            self.rect.right = ssize[0]
            self.speed[0] = 0



class Mob(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.surface.Surface((30,40))
        self.image.fill((255,0,0))

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ssize[0]- self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = [random.randint(-3,3),\
                      random.randint(0,7)]


    def update(self):
        for i in [0,1]:
            self.rect[i] += self.speed[i]




#object inits
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# generate mobs
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# loop setup
running = True
# game loop
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

    # display
    screen.fill((255,255,255))
    all_sprites.draw(screen)

    pygame.display.flip()

pygame.quit()
