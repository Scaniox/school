import pygame as pg

tsize = 64
ssize = [tsize*15, tsize*10]

fps = 120

bg_col = (0,60, 200)

level_file = "lvl.txt"
asset_paths = {"p" : [r"platformerGraphicsDeluxe_Updated/Tiles/grass.png"],
               "f" : [r"platformerGraphicsDeluxe_Updated/Items/flagYellow2.png", r"platformerGraphicsDeluxe_Updated/Items/flagYellowHanging.png"],
               "player" : [r"C:/Users/alexl/Documents/GitHub/school/pygame/side scroller game/img/platformerGraphicsDeluxe_Updated/Player/p2_jump.png"]  }

friction = 0.99
grav = 1500
player_acc = 1500
jump_power = 1000

camera_edge_padding = 100
