# main file to run the tile based game
# modules
import pygame as pg, random
from settings import *
from sprites import *
from pathlib import Path


class Game():
    def __init__(self):
        pg.init()
        pg.mixer.init()
        pg.key.set_repeat(100)

        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode(ssize)

        self.clock = pg.time.Clock()

        self.load_data()
        self.running = True


    def load_data(self):
        # load map data
        self.map_data = []
        root = Path(__file__).parent

        with (root / "map.txt") as file:
            for line in file.read_text().split("\n"):
                self.map_data.append(line)


    def new(self):
        # groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.LayeredUpdates()

        # generate sprites from map file
        for row_index, row in enumerate(self.map_data):
            for column_index, tile in enumerate(row):

                if tile == "1":
                    Wall(self, column_index, row_index)

                elif tile == "P":
                    self.player = Player(self, column_index, row_index)


    def run(self):
        # game loop
        #pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(fps) / 1000
            self.events()
            self.update()
            self.draw()


    def events(self):
        self.screen.fill(BG_COLOUR)

        # handle game events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                self.playing = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.Playing = False


    def update(self):
        # game loop - update
        self.all_sprites.update()


    def draw_grid(self):
        for x in range(0, ssize[0], tsize[0]):
            pg.draw.line(self.screen, (200,200,200), (x,0), (x, ssize[1]))
        for y in range(0, ssize[1], tsize[1]):
            pg.draw.line(self.screen, (200,200,200), (0, y), (ssize[0], y))


    def draw(self):
        #game loop - draw
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()


    def show_start_screen(self):
        pass


    def show_go_screen(self):
        pass


    def wait_for_key(self):
        # delay until a key is pressed
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False

                if event.type == pg.KEYUP:
                    waiting = False


    def draw_text(self, text, size, color, x, y):
        # draws text
        font = pg.font.Font(self.FONT_NAME, size)
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
