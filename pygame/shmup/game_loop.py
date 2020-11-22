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



class game():
    def __init__(self):
        self.reset()

    def reset(self):
        #¬ group generation
        self.groups = {  "all_sprites" : pygame.sprite.Group(),
                    "mobs" : pygame.sprite.Group(),
                    "bullets" : pygame.sprite.Group(),
                    "powerups" : pygame.sprite.Group(), }


        #¬ generate player
        self.player = Player(self.groups)
        self.groups["all_sprites"].add(self.player)

        #¬ generate mobs
        for i in range(8):
            m = Mob()
            self.groups["all_sprites"].add(m)
            self.groups["mobs"].add(m)


    def run(self, screen, loop_history):
        global score
        # list of arguments to feed back to controller
        feedback = []

        #handle loop history:
        if loop_history[-2] == "start":
            loop_history.append("game")
            self.reset()

        # events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                feedback.append("exit")

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                feedback.append("switch:pause")

        # update
        self.groups["all_sprites"].update()

        #collisions
        #¬ bullet - mob collision
        hits = pygame.sprite.groupcollide(self.groups["mobs"], self.groups["bullets"], False, True)
        for hit_mob in hits:
            #score
            score += round(100 - hit_mob.radius)

            # explosions
            expl = Explosion(hit_mob.rect.center, "L")
            self.groups["all_sprites"].add(expl)
            random.choice(meteor_expl_snd).play()

            # spawn powerups
            if random.random() > 0.9:
                pow = Pow(hit_mob.rect.center)
                self.groups["all_sprites"].add(pow)
                self.groups["powerups"].add(pow)

            hit_mob.respawn()

        #¬ mob - player collision
        hits = pygame.sprite.spritecollide(self.player, self.groups["mobs"], False, pygame.sprite.collide_circle)
        for hit_mob in hits:
            # reduce shield
            self.player.shield -= hit_mob.radius

            # cause player death
            if self.player.shield <= 0:
                self.death_expl = Explosion(self.player.rect.center, "P")
                self.groups["all_sprites"].add(self.death_expl)
                die_sound.play()
                self.player.hide()
                self.player.lives -= 1
                self.player.shield = 100

                # respawn meteotrs:
                for mob in self.groups["mobs"]:
                    mob.respawn()

            expl = Explosion(hit_mob.rect.center, "S")
            self.groups["all_sprites"].add(expl)
            hit_mob.respawn()

        # powerup player collide
        hits = pygame.sprite.spritecollide(self.player, self.groups["powerups"], True)
        for hit_p_up in hits:
            # shield power up
            if hit_p_up.type == "shield":
                self.player.shield = min(100, self.player.shield + random.randint(10,30))
                shield_p_up_sound.play()

            # gun power up
            elif hit_p_up.type == "gun":
                self.player.powerup()
                gun_p_up_sound.play()

        # end game check
        if self.player.lives == 0 and not self.death_expl.alive():
            feedback.append("switch:start")
            saved_background = screen.copy()

        # display
        screen.blit(scaled_background, [0,0])
        self.groups["all_sprites"].draw(screen)

        draw_text(screen, str(score), (200,200,0), 28, (ssize[0]//2, 15))
        draw_bar(screen, [5,5], self.player.shield)
        draw_lives(screen, [ssize[0]-100, 10], self.player.lives, player_live_img)

        return feedback
