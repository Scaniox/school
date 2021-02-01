import pygame as pg
import config as cfg
from classes import *
from functions import *
from pathlib import Path

vec2 = pg.math.Vector2

class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(cfg.ssize)
        self.clock = pg.time.Clock()

        # sprite groups
        self.update_sprites = pg.sprite.Group()
        self.draw_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()


        # load assets:
        img_folder = (Path(__file__).parent) / "img"
        self.player_img = pg.image.load(str(img_folder / cfg.asset_paths["player"][0])).convert_alpha()
        self.wall_img = pg.image.load(str(img_folder / cfg.asset_paths["p"][0])).convert_alpha()
        #pg.image.load(str(img_folder / path)).convert_alpha()
        self.flag_imgs = [pg.image.load(str(img_folder / path)).convert_alpha() for path in cfg.asset_paths["f"]]

        self.bsize = [0, 0]

        # load level
        with open("lvl.txt", "r") as level_file:
            lines = level_file.readlines()
            self.bsize = [len(lines[0])-1, len(lines)]
            for row, line in enumerate(lines):
                for column, block in enumerate(line):
                    #print(block)
                    pos = vec2(column, row)
                    if block == "p":
                        Block(self, vec2(pos))
                    elif block == "s":
                        self.player = Player(self, vec2(pos))
                    elif block == "f":
                        Flag(self, vec2(pos))

        self.camera = Camera(self, self.player)

        self.run()


    def run(self):
        self.running = True
        while self.running:
            # timing
            self.dt = self.clock.tick(cfg.fps) / 1000
            self.events()
            self.update()
            self.draw()

    def events(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False


    def update(self):
        self.update_sprites.update()


    def draw(self):
        self.screen.fill(cfg.bg_col)
        for sprite in self.draw_sprites:
            self.screen.blit(sprite.image, self.camera.transform_rect(sprite.rect))
        pg.display.flip()


Game()
