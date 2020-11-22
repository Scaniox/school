# this file is responsible for importing assets for other files to use
import pygame, random
from pathlib import Path
from config import *


pygame.mixer.init()
pygame.init()
screen = pygame.display.set_mode([1,1]) # screen for converting assets

#¬ image asset init
background_img = pygame.image.load(str(img_dir / "background_blue.png")).convert()
scaled_background = pygame.transform.scale(background_img, ssize)

player_img = pygame.image.load(str(img_dir / "playerShip1_blue.png")).convert()
player_live_img = pygame.transform.scale(player_img.copy(), (25,19))
player_live_img.set_colorkey((0,0,0))

bullet_img = pygame.image.load(str(img_dir / "laserBlue01.png")).convert()

#¬¬ load all images in Meteors folder
meteor_imgs = []
for image in (img_dir / "Meteors").iterdir():
    img = pygame.image.load(str(image)).convert()
    img.set_colorkey((0,0,0))
    meteor_imgs.append(img)

#¬¬ explosion images
expl_anim = {}
expl_anim["S"] = []
expl_anim["L"] = []
expl_anim["P"] = []

for i in range(9):
    img = pygame.image.load(str(img_dir / "explosions" / f"regularExplosion0{i}.png")).convert()
    img.set_colorkey((0,0,0))
    expl_anim["L"].append(pygame.transform.scale(img, (75,75)))
    expl_anim["S"].append(pygame.transform.scale(img, (32,32)))

    img = pygame.image.load(str(img_dir / "explosions" / f"sonicExplosion0{i}.png")).convert()
    img.set_colorkey((0,0,0))
    expl_anim["P"].append(pygame.transform.scale(img, (150,150)))

#¬¬ powerup images
powerup_images = {}
powerup_images["shield"] = pygame.image.load(str(img_dir / "powerupGreen_shield.png")).convert()
powerup_images["gun"] = pygame.image.load(str(img_dir / "powerupRed_bolt.png")).convert()
for image in powerup_images.values():
    image.set_colorkey((0,0,0))

#¬ sound asset init
shoot_sound = pygame.mixer.Sound(str(snd_dir / "shoot.wav"))
die_sound = pygame.mixer.Sound(str(snd_dir / "ship explosion.wav"))
shield_p_up_sound = pygame.mixer.Sound(str(snd_dir / "shield regen.wav"))
gun_p_up_sound = pygame.mixer.Sound(str(snd_dir / "weapon upgrade.wav"))

#¬¬ meteor explosion sounds
meteor_expl_snd = [pygame.mixer.Sound(str(snd_dir / name)) for name in ["Explosion.wav","Explosion2.wav"]]

#¬¬ background music
"""pygame.mixer.music.load(str(snd_dir / "tgfcoder-FrozenJam-SeamlessLoop.ogg"))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play()"""
pygame.quit()
