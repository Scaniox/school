#"Yippee" song by Snabisch: http://opengameart.org/content/yippee-0
#"Happy Tune" song by syncopika: https://opengameart.org/content/happy-tune

# main file to run the jumpy platform game
# modules
import pygame as pg, random
from settings import *
from sprites import *
from pathlib import Path


class Game():
    def __init__(self):
        self.clock = pg.time.Clock()
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode(ssize)
        pg.display.set_caption(TITLE)
        self.running = True
        self.FONT_NAME = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        # load assets
        self.dir = Path(__file__).parent
        self.img_dir = self.dir / "img"
        self.snd_dir = self.dir / "snd"

        # load high score from file
        try:
            self.highscore = int((self.dir / HS_FILE).read_text())
        except:
            self.highscore = 0

        # load spritesheet
        self.spritesheet = Spritesheet(str(self.img_dir / SPRITE_SHEET))

        # load sound
        self.jump_sound = pg.mixer.Sound(str(self.snd_dir / "Jump8.wav"))
        self.boost_sound = pg.mixer.Sound(str(self.snd_dir / "boost.wav"))

    def new(self):
        # start a new game
        self.score = 0

        # groups
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()

        self.player = Player(self)

        for plat in platform_list:
            p = Platform(self, *plat)

        # music
        pg.mixer.music.load(str(self.snd_dir / "021914bgm2(happytune).wav"))

    def run(self):
        # game loop
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def events(self):
        # game loop - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                self.running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()

            elif event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def update(self):
        # game loop - update
        self.all_sprites.update()

        # collisions
        #¬ player platform collisions
        if self.player.vel.y > 0:
            # check for collisions (offset by 1)
            self.player.pos.y += 1
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            self.player.pos.y -= 1

            if hits:
                # collide with lowest platform
                lowest = max(hits, key=lambda hit: hit.rect.top)
                if lowest.rect.left-10 < self.player.pos.x < lowest.rect.right+10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False


        #¬ player powerup collisons
        hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for hit in hits:
            if hit.type == "boost":
                self.boost_sound.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

        # scrolling if player in top 1/4 of screen
        if self.player.rect.top <= ssize[1]/4:
            # move player down
            self.player.pos.y += max(abs(self.player.vel.y), 2)

            #move platforms down
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                # remove off screen platforms
                if plat.rect.top > ssize[1]:
                    plat.kill()
                    self.score += 1


        # die
        if self.player.rect.bottom > ssize[1]:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()

        if len(self.platforms) == 0:
            self.playing = False

        # spawn new platforms:
        while len(self.platforms) < 6:
            x = random.randrange(0, ssize[0]-1)
            y = random.randrange(-55, -30)
            p = Platform(self, x, y)

    def draw(self):
        #game loop - draw
        self.screen.fill(BG_COLOUR)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        self.draw_text(str(self.score), 22, (255,255,255), ssize[0]//2, 15)
        pg.display.flip()

    def show_start_screen(self):
        # game start screen

        # music
        pg.mixer.music.load(str(self.snd_dir / "Yippee.wav"))
        pg.mixer.music.play(loops=-1)

        self.screen.fill(BG_COLOUR)
        self.draw_text(TITLE, 40, (255,255,255), ssize[0]//2, ssize[1]/4 )
        self.draw_text("Arrows to move , space to jump", 22, (255,255,255), ssize[0]/2, ssize[1]/2)
        self.draw_text("press a key to start", 22, (255,255,255), ssize[0]/2, ssize[1]/2 + 30)
        self.draw_text(f"High Score: {self.highscore}", 22, (255,255,255), ssize[0]/2, 15)
        pg.display.flip()
        self.wait_for_key()

        pg.mixer.music.fadeout(500)

    def show_go_screen(self):
        # game over screen
        # skip if closing window so it closes instantly
        if not self.running:
            return

        # music
        pg.mixer.music.load(str(self.snd_dir / "Yippee.wav"))
        pg.mixer.music.play(loops=-1)

        self.screen.fill((255,0,0))
        self.draw_text("Game Over", 40, (255,255,255), ssize[0]//2, ssize[1] / 4 )
        self.draw_text(f"Score : {self.score}", 22, (255,255,255), ssize[0]/2, ssize[1] / 2)
        self.draw_text("press a key to play again", 22, (255,255,255), ssize[0] / 2, ssize[1] * 3/4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22 , (255,255,255), ssize[0] / 2, ssize[1] / 2 + 40)

            (self.dir / HS_FILE).write_text(str(self.score))
        else:
            self.draw_text(f"High Score: {self.highscore}", 22, (255,255,255), ssize[0] / 2, ssize[1] /2 + 40)

        pg.display.flip()
        self.wait_for_key()

        pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        # delay until a key is pressed
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False

                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        # draws text
        font = pg.font.Font(self.FONT_NAME, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.run()
    g.show_go_screen()
