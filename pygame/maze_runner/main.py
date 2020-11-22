# maze game

#modules-------------------------------------------------------------------------------------------
import pygame

#constants
ssize = (800,600)
fps = 30

#variables

#functions-----------------------------------------------------------------------------------------
#main method
def main():

    #pygame init
    pygame.init()
    screen = pygame.display.set_mode(ssize)
    pygame.display.set_caption("Maze Runner")

    #object inits
    clock = pygame.time.Clock()

    player = Player([50,50])

    moving_sprites = pygame.sprite.Group()
    moving_sprites.add(player)


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

        # display
        screen.fill((0,0,0))
        moving_sprites.draw(screen)

        pygame.display.flip()


#classes-------------------------------------------------------------------------------------------
class Wall(pygame.sprite.Sprite):
    def __init__(self, rect, colour):
        #parent constructor
        super().__init__()

        # image
        self.colour = colour
        self.image = pygame.surface.Surface(rect.size)
        self.image.fill(self.colour)

        # rect
        self.rect = self.image.get_rect()
        self.rect.center = rect.topleft



class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        # parent constructor
        super().__init__()

        # kinematics
        self.velocity = [0, 0]

        # image
        self.image = pygame.surface.Surface([15,15])
        self.image.fill((255,255,255))

        #rect
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def change_speed(self, vector):
        self.velocity = [self.velocity[i] + vector[i] for i in [0,1]]

    def move(self, walls):
        # add wall collisions
        hit_lit = pygame.sprite.spritecollide(self, walls, False)

        for i in [0,1]:
            # collisions
            for block in hit_list:
                # less size collisions
                if self.velocity[i] <= 0: # moving in -ve direction
                    self.velocity[i] = 0
                    self.rect[i] = block.rect[i] + block.rect[i+2]

                elif self.velocity[i] >= 0: # moving in +ve direction
                    self.velocity[i] = 0
                    self.rect[i] = block.rect[i] - self.rect[i+2]



            self.rect[i] += self.velocity[i]

        self.rect.center = self.pos



class Room1():
    pass



class Room2():
    pass



class Room3():
    pass

main()
pygame.quit()
