# this file contains the code run my the main game loop: the actuall gameplay

# modules
import pygame, random
from pathlib import Path
from config import *
from assets import *
from classes import *

#variables-----------------------------------------------------------------------------------------
global score
score = 0

#object inits--------------------------------------------------------------------------------------
#¬ group generation
groups = {  "all_sprites" : pygame.sprite.Group(),
            "mobs" : pygame.sprite.Group(),
            "bullets" : pygame.sprite.Group(),
            "powerups" : pygame.sprite.Group(), }


#¬ generate player
player = Player(groups)
groups["all_sprites"].add(player)

#¬ generate mobs
for i in range(8):
    m = Mob()
    groups["all_sprites"].add(m)
    groups["mobs"].add(m)



def run_game(screen):
    global score
    # list of arguments to feed back to controller
    feedback = []

    # events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            feedback.append("exit")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            feedback.append("switch:pause")

    # update
    groups["all_sprites"].update()

    #collisions
    #¬ bullet - mob collision
    hits = pygame.sprite.groupcollide(groups["mobs"], groups["bullets"], False, True)
    for hit_mob in hits:
        #score
        score += round(100 - hit_mob.radius)

        # explosions
        expl = Explosion(hit_mob.rect.center, "L")
        groups["all_sprites"].add(expl)
        random.choice(meteor_expl_snd).play()

        # spawn powerups
        if random.random() > 0.9:
            pow = Pow(hit_mob.rect.center)
            groups["all_sprites"].add(pow)
            groups["powerups"].add(pow)

        hit_mob.respawn()

    #¬ mob - player collision
    hits = pygame.sprite.spritecollide(player, groups["mobs"], False, pygame.sprite.collide_circle)
    for hit_mob in hits:
        # reduce shield
        player.shield -= hit_mob.radius

        # cause player death
        if player.shield <= 0:
            death_expl = Explosion(player.rect.center, "P")
            groups["all_sprites"].add(death_expl)
            die_sound.play()
            player.hide()
            player.lives -= 1
            player.shield = 100

        expl = Explosion(hit_mob.rect.center, "S")
        groups["all_sprites"].add(expl)
        hit_mob.respawn()

    # powerup player collide
    hits = pygame.sprite.spritecollide(player, groups["powerups"], True)
    for hit_p_up in hits:
        # shield power up
        if hit_p_up.type == "shield":
            player.shield = min(100, player.shield + random.randint(10,30))
            shield_p_up_sound.play()

        # gun power up
        elif hit_p_up.type == "gun":
            player.powerup()
            gun_p_up_sound.play()

    # end game check
    if player.lives == 0 and not death_expl.alive():
        game_state = "start"
        saved_background = screen.copy()

    # display
    screen.blit(scaled_background, [0,0])
    groups["all_sprites"].draw(screen)

    draw_text(screen, str(score), (200,200,0), 28, (ssize[0]//2, 15))
    draw_bar(screen, [5,5], player.shield)
    draw_lives(screen, [ssize[0]-100, 10], player.lives, player_live_img)

    return feedback
