# main file to run the jumpy platform game
# modules
import pygame as pg, random
from settings import *
from sprites import *


class Game():
    def __init__(self):
        self.clock = pg.time.Clock()
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode(ssize)
        pg.display.set_caption(title)
        self.running = True
        self.font_name = pg.font.match_font(font_name)


    # start a new game
    def new(self):
        self.score = 0

        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()

        self.player = Player(self)
        self.all_sprites.add(self.player)

        for plat in platform_list:
            p = Platform(*plat)
            self.all_sprites.add(p)
            self.platforms.add(p)


    # game loop
    def run(self):
        self.playing = True

        while self.playing:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()


    # game loop - events
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()


    # game loop - update
    def update(self):
        self.all_sprites.update()

        # collisions
        #¬ player platform collisions
        if self.player.vel.y > 0:
            # check for collisions (offset by 1)
            self.player.pos.y += 1
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            self.player.pos.y -= 1

            if hits:
                self.player.pos.y = hits[0].rect.top
                self.player.vel.y = 0

        # scrolling
        if self.player.rect.top <= ssize[1]/4:
            # move player down
            self.player.pos.y += abs(self.player.vel.y)

            #move platforms down
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                # remove off screen platforms
                if plat.rect.top > ssize[1]:
                    plat.kill()
                    self.score += 1


        # die
        if self.player.rect.bottom > ssize[1]:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platforms) == 0:
            self.playing = False

        # spawn new platforms:
        while len(self.platforms) < 6:
            width = random.randrange(50,100)
            x = random.randrange(0, ssize[0]-1)
            y = random.randrange(-75, -30)
            p = Platform(x, y, width, 20)

            self.all_sprites.add(p)
            self.platforms.add(p)


    #game loop - draw
    def draw(self):
        self.screen.fill((0,0,0))
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, (255,255,255), ssize[0]//2, 15)
        pg.display.flip()


    # game start screen
    def show_start_screen(self):
        pass


    # game over screen
    def show_go_screen(self):
        pass


    # draws text
    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.run()
    g.show_go_screen()
