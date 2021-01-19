import pygame as pg
from settings import *

class Map():
    def __init__(self, filepath):
        # load map data
        self.data = []

        with (filepath) as file:
            for line in file.read_text().split("\n"):
                self.data.append(line.strip())

        self.gsize = [len(self.data[0]), len(self.data)-1]
        self.ssize = [self.gsize[i] * tsize[i] for i in [0,1]]



class Camera():
    def __init__(self, size):
        self.camera = pg.Rect(0, 0, *size)
        self.size = size

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        self.camera.topleft = [-target.rect[i] + ssize[i]//2 for i in [0,1]]

        # limit scroll sizes
        self.camera.topleft = [max(min(self.camera[i], 0), -(self.size[i]- ssize[i])) for i in [0,1] ]
