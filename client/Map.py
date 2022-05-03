from settings import *
from os import path, sep
import pygame as pg


class Map:
    def __init__(self):
        game_folder = path.dirname(__file__)
        self.data = []
        with open(path.join(game_folder+sep, "map.txt"), 'rt') as f:
            for line in f:
                self.data.append(line.strip())
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

    def generateMap(self):
        """Generate blank map with walls as border into map.txt according to settings
        """
        with open("map.txt", "w") as f:
            f.write("1"*(MAP_WIDTH-1)+"1\n")
            for j in range(MAP_HEIGHT-2):
                f.write("1"+"."*(MAP_WIDTH-2)+"1\n")
            f.write("1"*(MAP_WIDTH-1)+"1\n")
        print("Map generated")


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + int(LEFTWIDTH/2)
        y = -target.rect.y + int(HEIGHT/2)
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width-LEFTWIDTH), x)  # right
        y = max(-(self.height-HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, LEFTWIDTH, self.height)
        
    def inCamera(self, rect):
        return pg.Rect((-self.camera.x,-self.camera.y,LEFTWIDTH,self.height)).colliderect(rect)
