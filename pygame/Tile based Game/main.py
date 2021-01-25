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
        snd_folder = root / "snd"

        self.map = TiledMap(map_folder / "level1.tmx")
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # player image
        self.player_img = pg.image.load(str(img_folder / PLAYER_IMG)).convert_alpha()
        # wall image
        self.wall_img = pg.image.load(str(img_folder / WALL_IMG)).convert_alpha()
        # zombie image
        self.mob_img = pg.image.load(str(img_folder / MOB_IMG)).convert_alpha()
        # bullet_imgs
        self.bullet_imgs = {}
        self.bullet_imgs["lg"] = pg.image.load(str(img_folder / BULLET_IMG)).convert_alpha()
        self.bullet_imgs["sm"] = pg.transform.scale(self.bullet_imgs["lg"], (10, 10))
        # splat image
        self.splat = pg.image.load(str(img_folder / SPLAT_IMAGE)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))
        # screen dimmer
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0,0,0,180))

        # muzzle flashes
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(str(img_folder / img)).convert_alpha())

        # ITEM_IMAGES
        self.item_imgs = {}
        for name, img in ITEM_IMAGES.items():
            self.item_imgs[name] = (pg.image.load(str(img_folder / img)).convert_alpha())

        # sounds
        pg.mixer.music.load(str(snd_folder / BG_MUSIC))
        # effects
        self.effects_sounds = {}
        for name, path in EFFECTS_SOUNDS.items():
            self.effects_sounds[name] = pg.mixer.Sound(str(snd_folder / path))
        # weapon sounds
        self.weapon_sounds = {}
        for weapon_name, snd_paths in WEAPON_SOUNDS.items():
            self.weapon_sounds[weapon_name] = []
            for path in snd_paths:
                snd = pg.mixer.Sound(str(snd_folder / path))
                snd.set_volume(0.3)
                self.weapon_sounds[weapon_name].append(snd)
        # zombie moan sounds
        self.zombie_moan_sounds = []
        for path in ZOMBIE_MOAN_SOUNDS:
            snd = pg.mixer.Sound(str(snd_folder / path))
            snd.set_volume(0.1)
            self.zombie_moan_sounds.append(snd)
        # zombie hit sounds
        self.zombie_hit_sounds = []
        for path in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(str(snd_folder / path)))
        # player hit sounds
        self.player_hit_sounds = []
        for path in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(str(snd_folder / path)))


    def new(self):
        # groups
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player":
                self.player = Player(self, tile_object.x//tsize[0], tile_object.y//tsize[1])

            elif tile_object.name == "wall":
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)

            elif tile_object.name == "zombie":
                Mob(self, tile_object.x//tsize[0], tile_object.y//tsize[1])

            elif tile_object.name in ["health", "shotgun"]:
                Item(self, [tile_object.x, tile_object.y], tile_object.name)

        # camera
        self.camera = Camera(self.map.ssize)
        self.paused = False
        self.effects_sounds["level_start"].play()


    def run(self):
        # game loop
        #pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(fps) / 1000
            self.events()
            if not self.paused:
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
                if event.key == pg.K_p:
                    self.paused = not self.paused


    def update(self):
        # game loop - update
        self.all_sprites.update()
        self.camera.update(self.player)

        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == "health" and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.player.add_health(HEALTH_PACK_AMOUNT)
                self.effects_sounds["health_up"].play()

            elif hit.type == "shotgun":
                hit.kill()
                self.player.weapon = "shotgun"
                self.effects_sounds["gun_pickup"].play()

        # mobs hitting players
        hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)

            if self.player.health <= 0:
                self.playing = False
        #¬ hit player back
        if hits:
            self.player.hit()
            self.player.vel += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
            random.choice(self.player_hit_sounds).play()

        # bullets hitting mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.health -= WEAPONS[self.player.weapon]["damage"] * len(hits[hit])
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

        if self.paused:
            self.screen.blit(self.dim_screen, (0,0))
            self.draw_text("PAUSED", 105, (255,0,0), *[i//2 for i in ssize])
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
