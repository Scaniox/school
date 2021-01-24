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
PLAYER_SPEED = 25
PLAYER_DRAG = 5
PLAYER_ROT_SPEED = 350
PLAYER_IMG = "topdown-shooter/PNG/Man Blue/manBlue_gun.png"
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

# gun settings
BULLET_IMG = "bullet.png"
BULLET_SPEED = 1000
BULLET_LIFETIME = 1000
BULLET_RATE = 150
BARREL_OFFSET = (20,10)
GUN_SPREAD = 5
KICKBACK = 0.5

# walls
WALL_IMG = "tileGreen_39.png"
WALL_DRAG = 0.999

# mobs
MOB_IMG = "topdown-shooter/PNG/Zombie 1/zoimbie1_hold.png"
MOB_SPEED = 4
MOB_DRAG = 1
MOB_HIT_RECT = pg.Rect(0,0, 30, 30)
