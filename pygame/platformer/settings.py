# game options and settings

#constants
TITLE = "Jumpy"
ssize = (480, 600)
fps = 60
FONT_NAME = "arial"
HS_FILE = "highscore.txt"
SPRITE_SHEET = "spritesheet_jumper.png"


# player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP_STRENGTH = 20

# game properties
BOOST_POWER = 60
PLAT_COUNT = 8
POW_SPAWN_PCT = 7
MOB_FREQ = 5000

# starting platforms
platform_list = [   (0, ssize[1] - 60),
                    (ssize[0]/2 - 50, ssize[1]* 3/4),
                    (125, ssize[1] - 350),
                    (350, 200),
                    (175, 100)]

# colour schemes
BG_COLOUR = (64,128,255)
