# game options and settings
import pygame as pg

#constants
TITLE = "tile"
ssize = (1024, 768)
tsize = [64, 64]
gsize = [ssize[i] / tsize[i] for i in [0,1]]
fps = 10000
FONT_NAME = "Arial"

# colour schemes
BG_COLOUR = (76, 45, 5)
DRAW_DEBUG = False


# player settings
PLAYER_SPEED = 25
PLAYER_DRAG = 5
PLAYER_ROT_SPEED = 350
PLAYER_IMG = "topdown-shooter/PNG/Man Blue/manBlue_gun.png"
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
PLAYER_HEALTH = 250

# gun settings
BULLET_IMG = "bullet.png"
BULLET_SPEED = 1000
BULLET_LIFETIME = 1000
BULLET_RATE = 150
BARREL_OFFSET = (20,10)
KICKBACK = 0.5
GUN_SPREAD = 5
BULLET_DAMAGE = 10

# walls
WALL_IMG = "tileGreen_39.png"
WALL_DRAG = 0.999

# mobs
MOB_IMG = "topdown-shooter/PNG/Zombie 1/zoimbie1_hold.png"
MOB_SPEED = 4
MOB_SPEED_UNCERTAINTY = 2
MOB_DRAG = 1
MOB_HIT_RECT = pg.Rect(0,0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 2
AVOID_RADIUS = 1
DISTANCING_FORCE = 0.3
DETECT_RADIUS = 8

# effects
MUZZLE_FLASHES = [f"smoke/whitePuff{i}.png" for i in [15,16,17,18]]
FLASH_DURATION = 40
SPLAT_IMAGE = "splat/splat green.png"

# layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# items
ITEM_IMAGES = {"health" : "health_pack.png"}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.06

# sounds
BG_MUSIC = "espionage.ogg"
PLAYER_HIT_SOUNDS = [f"pain/{i}.wav" for i in [8, 9, 10, 11]]
ZOMBIE_MOAN_SOUNDS = ["brains2.wav", "brains3.wav"] + [f"zombie-roar-{i}.wav" for i in range(1,7)]
ZOMBIE_HIT_SOUNDS = ["splat-15.wav"]
WEAPON_SOUNDS_GUN = ["sfx_weapon_singleshot2.wav"]
EFFECTS_SOUNDS = {"level_start" : "level_start.wav",
                  "health_up" : "health_pack.wav"}
