from engine import *

# block texture atlas
textures = { }

def name(): "pixelcraft"

def setup():
    textures['dirt'] = load_image('tiles/dirt.png')
    textures['grass'] = load_image('tiles/grass.png')

def draw():
    image(textures['dirt'], 0, 0)
    image(textures['grass'], 0, 40)