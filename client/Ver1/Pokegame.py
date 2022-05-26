
import random
import pygame as pg
import sys
import pickle
from os import path, sep
from settings import *
from Entities import *
from Map import *
from network import Network

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.network = None
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.network = Network()
        self.map = Map()
        img_folder = path.join(game_folder+sep,"sprites")
        self.MALE_SPRITE_SHEET = pg.image.load(path.join(img_folder+sep,"PlayerSprites"+sep,PLAYER_MALE_SPRITE)).convert_alpha()
        self.MALE_SPRITE_SHEET = pg.transform.scale(self.MALE_SPRITE_SHEET,(TILESIZE*4,TILESIZE*4))
        #self.MALE_SPRITE_SHEET.set_colorkey((0,0,0))
        self.FEMALE_SPRITE_SHEET = pg.image.load(path.join(img_folder+sep,"PlayerSprites"+sep,PLAYER_FEMALE_SPRITE)).convert_alpha()
        self.FEMALE_SPRITE_SHEET = pg.transform.scale(self.FEMALE_SPRITE_SHEET,(TILESIZE*4,TILESIZE*4))
        #self.FEMALE_SPRITE_SHEET.set_colorkey((0,0,0))
        self.TERRAIN_SPRITE_SHEET = pg.image.load(path.join(img_folder+sep,"TerrainSprites"+sep,TILESET)).convert_alpha()
        self.TERRAIN_SPRITE_SHEET = pg.transform.scale(self.TERRAIN_SPRITE_SHEET, (TILESIZE*8,int((TILESIZE*8)/(256))*9000))
        #self.TERRAIN_SPRITE_SHEET.set_colorkey((0,0,0))

    def new(self):
        """Starts a new game
        """
        self.all_sprites = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for y, row in enumerate(self.map.data):
            for x, cell in enumerate(row):
                if cell == WALL:
                    Wall(self, x, y)
                elif cell == EMPTYCELL:
                    Floor(self,x,y)
        self.spawnPlayer()
        self.camera = Camera(self.map.width, self.map.height)

    def spawnPlayer(self, x=-1, y=-1):
        """Spawn player, if no positional argument is passed or if invalid position argument, spawn randomly in valid cell
        Args:
            x (int, optional): Spawn coordiate x. Defaults to -1.
            y (int, optional): Spawn coordinate y. Defaults to -1.
        """
        player = Player(self, 0, 0,self.network.id,'f')
        while player.collides(x,y) or (x==-1 and y==-1):
            (x,y) = (random.randrange(1,MAP_WIDTH-1),random.randrange(1,MAP_HEIGHT-1))
        player.x = x 
        player.y = y
        self.player = player
        print(f"Player spawned at: {(x,y)}")

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        self.pollServer()
        
    def pollServer(self):
        serverRes = self.network.sendPlayerState(self.player)
        if serverRes:
            serverRes = pickle.loads(serverRes)
            # print("[CLIENT] polling server ",serverRes)
            for player in self.players:
                for id, pos in serverRes.items():
                    if player.id == id:
                        player.x = pos[0]
                        player.y = pos[1]
                    # else:
                    #     Player(self,pos[0],pos[1],id)
        
    def draw_grid(self):
        for x in range(0, LEFTWIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (LEFTWIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        for sprite in self.all_sprites:
          if self.camera.inCamera(sprite.rect):
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # for player in self.players:
        #     if self.camera.inCamera(player.rect):
        #         self.screen.blit(player.image, self.camera.apply(player))
        #self.draw_grid()
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_ESCAPE]:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
