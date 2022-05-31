
import random
import pygame as pg
import sys
import pickle
from os import path, sep
from settings import *
from Entities import *
from Map import *
from network import Network
import random
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
        self.pokemons = pg.sprite.Group()
        for y, row in enumerate(self.map.data):
            for x, cell in enumerate(row):
                if cell == WALL:
                    Wall(self, x, y)
                    # self.pokemons.add(PokemonDisplay(self,random.randint(0,50),('https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/31.png',x,y)))
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
        
        while self.collides(x,y) or (x==-1 and y==-1):
            (x,y) = (random.randrange(1,MAP_WIDTH-1),random.randrange(1,MAP_HEIGHT-1))
        player = Player(self,x,y,id=self.network.id)
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
        self.pokemons.update()
        self.camera.update(self.player)
        self.pollServer()

    def collides(self, x, y):
        collidables = pg.sprite.Group()
        collidables.add(self.walls)
        collidables.add(self.players)
        for entity in collidables:
            if entity.x == x and entity.y == y:
                return True
        return False
    def pollServer(self):
        serverRes = self.network.sendPlayerState(self.player)
        if serverRes:
            serverRes = pickle.loads(serverRes)
            ##  If Pokemon wave packet is replied from server:
            if "isPokemonPacket" in serverRes.keys():
                print("Pokemon packet recieved ")
                return 
            
            ## If other players' info is replied from server:
            resList = serverRes.keys()
            curPlayersIdList = [x.id for x in self.players.sprites()]
            print("[CLIENT] polling server ",serverRes)
            
            ## Check if server send caught pokemon
            if  "ID" in serverRes.keys():
                print("Successfully catch ",serverRes["name"])
                self.player.action = "MOVE"
                self.player.poketeam.append(serverRes)
                return
            
            ## Add new player
            for res in serverRes.keys():
                if res not in curPlayersIdList:
                    self.players.add(OtherPlayer(self,x=serverRes[res][0],y=serverRes[res][1],id=res,face=serverRes[res][2], action=serverRes[res][3],type='f')) 
            
            ## Update player position 
            for player in self.players:
                ## Remove disconnected players
                if player.id not in resList:
                    self.players.remove(player)
                else:
                    curPlayersIdList.append(player)
                for id, pos in serverRes.items():
                    if player.id == id:
                        player.x = pos[0]
                        player.y = pos[1]
                        player.face = pos[2]
                        player.action = pos[3]
            # print("Current player",self.players.sprites())
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


# g = Game()
# g.new()
# player = Player(g, 10,12,11,'m')
# player2 = Player(g, 11,12,111,'m')
# player3 = Player(g, 12,12,112,'m')

# gr = pg.sprite.Group()
# gr.add(player)
# gr.add(player2)
# gr.add(player3)
# for sprite in gr.sprites():
#     sprite.id = 11212
# gr.remove(player)
# for sprite in gr.sprites():
#     print(sprite.id)
