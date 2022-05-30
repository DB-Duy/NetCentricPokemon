# import pickle
# Pokemons_packet = {"isPokemonPacket": True}
# if "isPokemonPacket" in Pokemons_packet.keys():
#     print(True)
# else:
#      print(False)
     
# class Test:
#     def __init__(self):
#         self.a = 1
#         self.b = 2


# a = Test()
# b = pickle.dumps(a)
# c = pickle.loads(b)
# print(a.__dict__)
'''PG_image_url.py
load and display a web image using pygame and io

tested with Python27 and Python34  by  vegaseat  10mar2015
'''

import io
import pygame as pg
try:
    # Python2
    from urllib2 import urlopen
except ImportError:
    # Python3
    from urllib.request import urlopen

# initialize pygame
pg.init()

# on a webpage right click on the image you want and use Copy image URL
image_url = "http://matplotlib.org/_images/fill_demo.png"

image_str = urlopen(image_url).read()
# create a file object (stream)
image_file = io.BytesIO(image_str)

# (r, g, b) color tuple, values 0 to 255
white = (255, 255, 255)

# create a 600x400 white screen
screen = pg.display.set_mode((600,400),  pg.RESIZABLE )
screen.fill(white)

# load the image from a file or stream
image = pg.image.load(image_file)

# draw image, position the image ulc at x=20, y=20
screen.blit(image, (20, 20))

# nothing gets displayed until one updates the screen
pg.display.flip()

# start event loop and wait until
# the user clicks on the window corner x to exit
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit