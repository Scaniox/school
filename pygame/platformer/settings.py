# game options and settings

#constants
title = "Jumpy"
ssize = (480, 600)
fps = 60
font_name = "arial"
hs_file = "highscore.txt"

# player properties
player_acc = 0.5
player_friction = -0.12
player_grav = 0.8
player_jump_strength = 20

# starting platforms
platform_list = [   (0,ssize[1]-40, ssize[0], 40),
                    (ssize[0]/2 - 50, ssize[1]* 3/4, 100, 20),
                    (125, ssize[1] -350, 100, 20),
                    (350, 200, 100, 20),
                    (175, 100, 50, 20)]

# colour schemes
bg_colour = (64,128,255)
