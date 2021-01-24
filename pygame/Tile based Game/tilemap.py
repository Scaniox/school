import pygame as pg
from settings import *
import pytmx


class Map():
    def __init__(self, filepath):
        # load map data
        self.data = []

        with (filepath) as file:
            for line in file.read_text().split("\n"):
                self.data.append(line.strip())

        self.gsize = [len(self.data[0]), len(self.data)-1]
        self.ssize = [self.gsize[i] * tsize[i] for i in [0,1]]



class TiledMap():
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.ssize = [tm.width * tsize[0], tm.height * tsize[1]]
        self.tmxdata = tm


    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        tile = pg.transform.scale(tile, tsize)
                        surface.blit(tile, (x * tsize[0], y * tsize[1]))


    def make_map(self):
        temp_surface = pg.Surface(self.ssize)
        self.render(temp_surface)
        return temp_surface



class Camera():
    def __init__(self, size):
        self.camera = pg.Rect(0, 0, *size)
        self.size = size

    def apply(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        self.camera.topleft = [-target.rect.center[i] + ssize[i]//2 for i in [0,1]]

        # limit scroll sizes
        self.camera.topleft = [max(min(self.camera[i], 0), -(self.size[i]- ssize[i])) for i in [0,1] ]
