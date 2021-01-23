# game options and settings
import pygame as pg

#constants
TITLE = "tile"
ssize = (1024, 768)
fps = 10000
FONT_NAME = "Arial"

# colour schemes
BG_COLOUR = (76, 45, 5)



tsize = [64, 64]
gsize = [ssize[i] / tsize[i] for i in [0,1]]


# player settings
PLAYER_SPEED = 10
PLAYER_ROT_SPEED = 250
PLAYER_IMG = "topdown-shooter/PNG/Man Blue/manBlue_gun.png"
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

# walls
WALL_IMG = "tileGreen_39.png"
WALL_DRAG = 1

# mobs
MOB_IMG = "topdown-shooter/PNG/Zombie 1/zoimbie1_hold.png"
MOB_SPEED = 6
MOB_HIT_RECT = pg.Rect(0,0, 30, 30)
