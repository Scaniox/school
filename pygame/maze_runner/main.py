# maze game

# modules-------------------------------------------------------------------------------------------
import pygame

# constants
ssize = (800, 600)
fps = 60

# variables

# functions-----------------------------------------------------------------------------------------
# main method
def main():
    # pygame init
    pygame.init()
    screen = pygame.display.set_mode(ssize)
    pygame.display.set_caption("Maze Runner")

    # object inits
    clock = pygame.time.Clock()

    player = Player([50, 50])

    moving_sprites = pygame.sprite.Group()
    moving_sprites.add(player)

    # addr rooms = Start Here
    rooms = []

    room = Room1()
    rooms.append(room)
    room = Room2()
    rooms.append(room)
    room = Room3()
    rooms.append(room)

    current_room_no = 0
    current_room = rooms[current_room_no]

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

            if event.type == pygame.KEYDOWN:#
                if event.key == pygame.K_LEFT:
                    player.change_speed([-5, 0])
                if event.key == pygame.K_RIGHT:
                    player.change_speed([5, 0])
                if event.key == pygame.K_UP:
                    player.change_speed([0, -5])
                if event.key == pygame.K_DOWN:
                    player.change_speed([0, 5])

            if event.type == pygame.KEYUP:#
                if event.key == pygame.K_LEFT:
                    player.change_speed([5, 0])
                if event.key == pygame.K_RIGHT:
                    player.change_speed([-5, 0])
                if event.key == pygame.K_UP:
                    player.change_speed([0, 5])
                if event.key == pygame.K_DOWN:
                    player.change_speed([0, -5])

        # update
        player.move(current_room.wall_list)

        if player.rect.x > ssize[0]:
            current_room_no = (current_room_no + 1) % 3
            current_room = rooms[current_room_no]
            player.rect.x = 5

        if player.rect.x < 0 :
            current_room_no = (current_room_no - 1) % 3
            current_room = rooms[current_room_no]
            player.rect.x = ssize[0]-5

        # display
        screen.fill((0,0,0))
        current_room.wall_list.draw(screen)
        moving_sprites.draw(screen)

        pygame.display.flip()


# classes-------------------------------------------------------------------------------------------
class Wall(pygame.sprite.Sprite):
    def __init__(self, rect, colour):
        # parent constructor
        super().__init__()
        rect = pygame.rect.Rect(rect)

        # image
        self.colour = colour
        self.image = pygame.surface.Surface(rect.size)
        self.image.fill(self.colour)

        # rect
        self.rect = self.image.get_rect()
        self.rect.topleft = rect.topleft


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        # parent constructor
        super().__init__()

        # kinematics
        self.velocity = [0, 0]

        # image
        self.image = pygame.surface.Surface([15, 15])
        self.image.fill((255, 255, 255))

        # rect
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def change_speed(self, vector):
        self.velocity = [self.velocity[i] + vector[i] for i in [0, 1]]

    def move(self, walls):
        # add wall collisions
        hit_list = pygame.sprite.spritecollide(self, walls, False)

        for i in [0,1]:
            # collisions
            for block in hit_list:
                # less size collisions
                if self.velocity[i] < 0: # moving in -ve direction
                    self.rect[i] = block.rect[i] + block.rect[i+2]

                elif self.velocity[i] > 0: # moving in +ve direction
                    self.rect[i] = block.rect[i] - self.rect[i+2]


            self.rect[i] += self.velocity[i]


class Room():
    #base class for all rooms
    wall_list = None
    enemy_list = None

    def __init__(self):
        self.wall_list = pygame.sprite.Group()



class Room1(Room):
    def __init__(self):
        super().__init__()

        #each wall will need a x, y, w, h, colour
        border_colour = (255,255,255)
        walls_information = [   [0, 0, 20, 250, border_colour],
                                [0, 350, 20, 250, border_colour],
                                [780, 0, 20, 250, border_colour],
                                [780, 350, 20, 250, border_colour],
                                [20, 0, 760, 20, border_colour],
                                [20, 580, 760, 20, border_colour],
                                [390, 50, 20 ,500, (0,0,255)]       ]

        walls = []
        for wall_data in walls_information:
            wall = Wall(wall_data[:4], wall_data[4])
            self.wall_list.add(wall)


class Room2(Room):
    def __init__(self):
        super().__init__()

        #each wall will need a x, y, w, h, colour
        border_colour = (255,255,0)
        walls_information = [   [0, 0, 20, 250, border_colour],
                                [0, 350, 20, 250, border_colour],
                                [780, 0, 20, 250, border_colour],
                                [780, 350, 20, 250, border_colour],
                                [20, 0, 760, 20, border_colour],
                                [20, 580, 760, 20, border_colour],
                                [190, 50, 20, 500, (0,255,0)],
                                [590, 50, 20, 500, (0,255,0)]   ]

        for wall_data in walls_information:
            wall = Wall(wall_data[:4], wall_data[4])
            self.wall_list.add(wall)



class Room3(Room):
    def __init__(self):
        super().__init__()

        #each wall will need a x, y, w, h, colour
        border_colour = (255,128,128)
        walls_information = [   [0, 0, 20, 250, border_colour],
                                [0, 350, 20, 250, border_colour],
                                [780, 0, 20, 250, border_colour],
                                [780, 350, 20, 250, border_colour],
                                [20, 0, 760, 20, border_colour],
                                [20, 580, 760, 20, border_colour]    ]

        walls = []
        # make red walls
        for x in range(100, 800, 100):
            wall_1 = Wall([x, 50, 20, 200], (255,0,0))
            wall_2 = Wall([x, 250, 20, 200], (255,0,0))
            walls += [wall_1, wall_2]

        # while walls
        for x in range(150, 700, 100):
            wall1 = Wall([x, 150, 20, 200], (255,255,255))
            walls.append(wall1)

        for wall_data in walls_information:
            wall = Wall(wall_data[:4], wall_data[4])
            self.wall_list.add(wall)

main()
pygame.quit()
