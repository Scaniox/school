# main file to run the tile based game
# modules
import pygame as pg, random
from settings import *
from sprites import *
from pathlib import Path
from tilemap import *

# HUD functions
def draw_player_health(surf, x, y, pct):
    pct = max(0, pct)

    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    col = (0,255,0) if pct > 0.6 else (255,255,0) if pct > 0.3 else (255,0,0)
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, (255,255,255), outline_rect, 2)

class Game():
    def __init__(self):
        pg.init()
        pg.mixer.init()
        pg.key.set_repeat(100)

        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode(ssize)

        self.clock = pg.time.Clock()

        self.load_data()
        self.running = True
        self.playing = True


    def load_data(self):
        # load map data
        root = Path(__file__).parent
        img_folder = root / "img"
        map_folder = root / "maps"

        self.map = TiledMap(map_folder / "level1.tmx")
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # player image
        self.player_img = pg.image.load(str(img_folder / PLAYER_IMG)).convert_alpha()
        # wall image
        self.wall_img = pg.image.load(str(img_folder / WALL_IMG)).convert_alpha()
        # zombie image
        self.mob_img = pg.image.load(str(img_folder / MOB_IMG)).convert_alpha()
        # bullet_img
        self.bullet_img = pg.image.load(str(img_folder / BULLET_IMG)).convert_alpha()

        # muzzle flashes
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(str(img_folder / img)).convert_alpha())


    def new(self):
        # groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player":
                self.player = Player(self, tile_object.x//tsize[0], tile_object.y//tsize[1])

            elif tile_object.name == "wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

            elif tile_object.name == "zombie":
                Mob(self, tile_object.x//tsize[0], tile_object.y//tsize[1])

        # camera
        self.camera = Camera(self.map.ssize)


    def run(self):
        # game loop
        #pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(fps) / 1000
            self.events()
            self.update()
            self.draw()


    def events(self):
        self.screen.fill(BG_COLOUR)

        # handle game events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                self.playing = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False


    def update(self):
        # game loop - update
        self.all_sprites.update()
        self.camera.update(self.player)

        # mobs hitting players
        hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)

            if self.player.health <= 0:
                self.playing = False
        # hit player back
        if hits:
            self.player.vel += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)

        # bullets hitting mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)


    def draw_grid(self):
        for x in range(0, ssize[0], tsize[0]):
            pg.draw.line(self.screen, (200,200,200), (x,0), (x, ssize[1]))
        for y in range(0, ssize[1], tsize[1]):
            pg.draw.line(self.screen, (200,200,200), (0, y), (ssize[0], y))


    def draw(self):
        #game loop - draw
        pg.display.set_caption(f"tile game: {self.clock.get_fps():.2f}fps")

        self.screen.blit(self.map_img, self.camera.apply(self.map_rect))

        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))

        if DRAW_DEBUG:
            for sprite in self.all_sprites:
                pg.draw.rect(self.screen, (0,255,255), self.camera.apply(sprite.hit_rect), 1)
            for sprite in self.walls:
                pg.draw.rect(self.screen, (0,255,255), self.camera.apply(sprite.hit_rect), 1)

        # HUD
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        pg.display.flip()


    def show_start_screen(self):
        pass


    def show_go_screen(self):
        pass


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


    def draw_text(self, text, size, colour, x, y):
        # draws text
        font = pg.font.Font(pg.font.match_font(FONT_NAME), size)
        text_surface = font.render(str(text), True, colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.run()
    g.show_go_screen()
