from engine import *

from camera import Camera
from world import World
from tile import Tile


camera = None
world = None

def setup():
    global camera, world

    rename('pixelcraft')
    resize(1000, 800)

    camera = Camera()
    world = World(Tile.Registry('data/tiles.toml'))

    world[0, 0] = 'grass'

def draw():
    camera.render(world)
    camera.x += 0.01
    camera.y += 0.005