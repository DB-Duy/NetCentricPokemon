import random
import pygame as pg
from settings import *
import io
from urllib.request import urlopen

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y,id,face="DOWN",action="MOVE", type='m'):
        """Creates and inserts player into game
    
        Args:
            game (Game): Game to insert player into
            x (int): x position
            y (int): y position
            face (str,optional): to change sprite image 
            action (str, optional): player actions ( MOVE, CATCH)
            type (str, optional): Sprite type, 'm' is male 'f' is female. Defaults to 'm'.
            id: playerID
        """
   
        self.id = id
        self.groups = [game.all_sprites, game.players]
        super().__init__(self.groups)
        self.game = game
        if type == 'f':
            self.sheet = game.FEMALE_SPRITE_SHEET
        else:
            self.sheet = game.MALE_SPRITE_SHEET
        self.image = pg.Surface((TILESIZE, TILESIZE),pg.SRCALPHA)
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect()
        self.direction = pg.math.Vector2()
        self.x = x
        self.y = y
        self.facing = face
        self.action = action
        self.unmoved = 0
        self.unmoved_frames = 0
        
        ## Player pokemon inventory
        self.poketeam = []
    def input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] or keys[pg.K_w]:
            if self.unmoved == 0:
                self.direction.y = -1
                self.facing = "UP"
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            if self.unmoved == 0:
                self.direction.y = 1
                self.facing = "DOWN"
        else:
            self.direction.y = 0

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            if self.unmoved == 0:
                self.direction.x = -1
                self.facing = "LEFT"

        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            if self.unmoved == 0:
                self.direction.x = 1
                self.facing = "RIGHT"
        elif keys[pg.K_SPACE]:
            self.action = f"CATCH {random.randint(1,50)}"
        else:
            self.direction.x = 0

    def drawSprite(self):
        self.image.fill((0, 0, 0, 0))
        if self.facing == "UP":
            self.image.blit(self.sheet, (0, 0), (self.unmoved*TILESIZE,
                            TILESIZE * 3, int(TILESIZE*IMG_SCALE), int(TILESIZE*IMG_SCALE)))
        elif self.facing == "DOWN":
            self.image.blit(self.sheet, (0, 0), (self.unmoved*TILESIZE,
                            TILESIZE * 0, int(TILESIZE*IMG_SCALE), int(TILESIZE*IMG_SCALE)))
        elif self.facing == "LEFT":
            self.image.blit(self.sheet, (0, 0), (self.unmoved*TILESIZE,
                            TILESIZE * 1, int(TILESIZE*IMG_SCALE), int(TILESIZE*IMG_SCALE)))
        else:
            self.image.blit(self.sheet, (0, 0), (self.unmoved*TILESIZE,
                            TILESIZE * 2, int(TILESIZE*IMG_SCALE), int(TILESIZE*IMG_SCALE)))

    def move(self):
        if self.unmoved_frames <= 0 and self.direction:
            if not self.collides(self.direction.x+self.x, self.direction.y+self.y):
                self.x += self.direction.x
                self.y += self.direction.y
                self.unmoved_frames = PLAYER_FRAMES_PER_STEP * 4 - 1
            else:
                self.unmoved = 0
        else:
            self.unmoved_frames = max(0, self.unmoved_frames-1)
            if((self.unmoved_frames+1)%PLAYER_FRAMES_PER_STEP==0):
              self.rect.x = self.x * TILESIZE - \
                  int(self.unmoved*self.direction.x*1/4*TILESIZE)
              self.rect.y = self.y * TILESIZE - \
                  int(self.unmoved*self.direction.y*1/4*TILESIZE)
        
        self.unmoved = int(self.unmoved_frames/PLAYER_FRAMES_PER_STEP)

    def collides(self, x, y):
        collidables = pg.sprite.Group()
        collidables.add(self.game.walls)
        collidables.add(self.game.players)
        for entity in collidables:
            if entity.x == x and entity.y == y:
                return True
        return False

    def update(self):
        self.input()
        self.move()
        self.drawSprite()

class OtherPlayer(Player):
    def __init__(self, game, x, y,id,face="DOWN",action="MOVE", type='m'):
        super().__init__(game, x, y,id,face,action, type)
    



class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        super().__init__(self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE)).convert_alpha()
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class PokemonDisplay(pg.sprite.Sprite):
    def __init__(self, game,ID,displayInfo):
        self.ID = ID
        url, x , y = displayInfo
       
        # create a file object (stream)
        # image_file = io.BytesIO(image_str)
        # image_str = urlopen(url).read()
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        # self.image = pg.image.load(image_file)
        self.image = pg.Surface((TILESIZE, TILESIZE)).convert_alpha()
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Floor(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        super().__init__(self.groups)
        self.game = game
        self.sheet = self.game.TERRAIN_SPRITE_SHEET
        self.image = pg.Surface((TILESIZE, TILESIZE)).convert_alpha()
        self.image.set_colorkey((0,0,0,0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.assignTile()

    def assignTile(self):
        self.image.blit(self.sheet, (0,0), (0,0,TILESIZE,TILESIZE))
      

    def update(self):
        pass
